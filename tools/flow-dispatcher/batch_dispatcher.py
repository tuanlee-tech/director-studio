#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
batch_dispatcher.py — Google Flow Multi-Account Batch Dispatcher (CDP)
Tự động hóa dispatch prompt và cào asset từ 5 tài khoản Google Flow song song.

Hỗ trợ:
  • python batch_dispatcher.py --status             (Xem tiến độ tổng thể các scene)
  • python batch_dispatcher.py --wave 2             (Chạy đợt 5 cảnh tiếp theo)
  • python batch_dispatcher.py --auto               (Chạy tự động liên tục các wave còn thiếu)
"""

import sys
import os
import json
import time
import base64
import shutil
import argparse
import subprocess
import urllib.request
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# UTF-8 stdout cho Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

try:
    import websocket
except ImportError:
    print("❌ Thiếu websocket-client. Vui lòng chạy: pip install websocket-client")
    sys.exit(1)


# 5 Cổng CDP tương ứng với 5 account Google Flow
ACCOUNT_PORTS = {
    1: 9223,
    2: 9224,
    3: 9225,
    4: 9226,
    5: 9227
}


class FlowCDPClient:
    def __init__(self, port, acc_id):
        self.port = port
        self.acc_id = acc_id
        self.ws = None
        self._msg_id = 0

    def connect(self):
        url = f"http://127.0.0.1:{self.port}/json/list"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            tabs = json.loads(resp.read().decode())

        flow_tab = next((t for t in tabs if "flow.google.com" in t.get("url", "")), None)
        if not flow_tab:
            pages = [t for t in tabs if t.get("type") == "page"]
            flow_tab = pages[0] if pages else None

        if not flow_tab:
            raise RuntimeError(f"Không tìm thấy tab nào trên port {self.port}")

        ws_url = flow_tab.get("webSocketDebuggerUrl")
        self.ws = websocket.create_connection(ws_url, timeout=15)
        self.send_cdp("Runtime.enable")
        self.send_cdp("Page.enable")
        return True

    def close(self):
        if self.ws:
            try:
                self.ws.close()
            except Exception:
                pass
            self.ws = None

    def send_cdp(self, method, params=None):
        self._msg_id += 1
        cid = self._msg_id
        payload = {"id": cid, "method": method, "params": params or {}}
        self.ws.send(json.dumps(payload))

        start = time.time()
        while time.time() - start < 15:
            msg = self.ws.recv()
            if not msg:
                continue
            data = json.loads(msg)
            if data.get("id") == cid:
                if "error" in data:
                    raise RuntimeError(f"CDP {method} error: {data['error'].get('message')}")
                return data.get("result", {})
        return {}

    def evaluate(self, expr, await_promise=False):
        res = self.send_cdp("Runtime.evaluate", {
            "expression": expr,
            "returnByValue": True,
            "awaitPromise": await_promise
        })
        val = res.get("result", {})
        return val.get("value")

    def get_existing_image_urls(self):
        """Lấy danh sách tất cả các ảnh hiện có trên trang để làm baseline."""
        js = """
        (() => {
            return Array.from(document.querySelectorAll('img'))
                .map(i => i.src)
                .filter(s => s && s.startsWith('http') && !s.includes('lh3.google') && !s.includes('gstatic'));
        })()
        """
        return set(self.evaluate(js) or [])

    def inject_and_submit_prompt(self, prompt_text):
        """Bước 3: Nhập prompt vào ProseMirror và bấm Enter đúng 1 lần duy nhất."""
        escaped = json.dumps(prompt_text)
        js = f"""
        (() => {{
            const el = document.querySelector('.ProseMirror') || 
                       document.querySelector('[aria-label*="What do you want to create"]') ||
                       document.querySelector('textarea');
            if (!el) return {{ success: false, error: 'Không tìm thấy ô nhập prompt' }};

            el.focus();
            document.execCommand('selectAll', false, null);
            document.execCommand('insertText', false, {escaped});
            el.dispatchEvent(new InputEvent('input', {{ bubbles: true }}));
            return {{ success: true }};
        }})()
        """
        r = self.evaluate(js)
        if not r or not r.get("success"):
            raise RuntimeError(f"Không thể điền prompt: {r.get('error') if r else 'Unknown'}")

        time.sleep(0.4)

        # Thử click nút "Start generation" hoặc "Tạo" trước
        js_click_btn = """
        (() => {
            const btn = document.querySelector('button[aria-label*="Start generation" i]') ||
                        document.querySelector('button.generate-icon-button') ||
                        document.querySelector('button[aria-label*="Tạo" i]');
            if (btn && !btn.disabled) {
                btn.click();
                return true;
            }
            return false;
        })()
        """
        btn_clicked = self.evaluate(js_click_btn)
        if not btn_clicked:
            # Fallback: Dispatch Enter key (rawKeyDown + keyUp)
            self.send_cdp("Input.dispatchKeyEvent", {
                "type": "rawKeyDown",
                "windowsVirtualKeyCode": 13,
                "unmodifiedText": "\r",
                "text": "\r",
                "key": "Enter",
                "code": "Enter"
            })
            self.send_cdp("Input.dispatchKeyEvent", {
                "type": "keyUp",
                "windowsVirtualKeyCode": 13,
                "unmodifiedText": "\r",
                "text": "\r",
                "key": "Enter",
                "code": "Enter"
            })
        return True

    def poll_for_new_image(self, baseline_urls, timeout=120):
        """
        Bước 4: Giám sát quá trình sinh ảnh và lấy URL ảnh mới tạo (hỗ trợ đa ngôn ngữ EN / VI).
        """
        start = time.time()
        time.sleep(3)  # Đợi 3s ban đầu

        while time.time() - start < timeout:
            js_check = """
            (() => {
                const stopBtn = document.querySelector('button[aria-label*="Stop" i], button[aria-label*="Cancel" i], button[aria-label*="Dừng" i], button[aria-label*="Hủy" i]');
                const isRunning = stopBtn !== null && stopBtn.offsetParent !== null;

                const currentImgs = Array.from(document.querySelectorAll('img'))
                    .map(i => i.src)
                    .filter(s => s && s.startsWith('http') && !s.includes('lh3.google') && !s.includes('gstatic'));

                return {
                    is_running: isRunning,
                    images: Array.from(new Set(currentImgs))
                };
            })()
            """
            st = self.evaluate(js_check) or {}
            is_running = st.get("is_running", False)
            current_imgs = set(st.get("images", []))

            # Tìm ảnh mới xuất hiện so với baseline
            new_imgs = list(current_imgs - baseline_urls)
            candidate_imgs = [u for u in new_imgs if "flow.google.com/asb/" in u or "flow-content.google" in u or "googleusercontent" in u or len(u) > 60]

            elapsed = int(time.time() - start)

            # Điều kiện xong: Có ảnh mới và agent đã ngừng chạy
            if candidate_imgs and not is_running:
                return candidate_imgs[-1]

            # Hoặc sau 20s nếu đã có ảnh mới xuất hiện
            if candidate_imgs and elapsed > 20 and not is_running:
                return candidate_imgs[-1]

            time.sleep(2.5)

        # Fallback sau timeout
        st = self.evaluate(js_check) or {}
        all_imgs = [u for u in st.get("images", []) if "flow.google.com/asb/" in u or "flow-content.google" in u or "googleusercontent" in u or len(u) > 60]
        if all_imgs:
            return all_imgs[-1]

        return None

    def fetch_image_bytes_in_browser(self, image_url):
        """Tải ảnh an toàn bằng fetch() trong context trình duyệt (mang theo session cookie)."""
        js = f"""
        (async () => {{
            const res = await fetch("{image_url}");
            const blob = await res.blob();
            return new Promise((resolve) => {{
                const reader = new FileReader();
                reader.onloadend = () => resolve(reader.result);
                reader.readAsDataURL(blob);
            }});
        }})()
        """
        data_url = self.evaluate(js, await_promise=True)
        if data_url and data_url.startswith("data:"):
            _, b64_str = data_url.split(",", 1)
            return base64.b64decode(b64_str)
        return None


def parse_prompts_file(prompts_file: Path):
    """Phân tích prompts.md và lấy danh sách các tác vụ tạo ảnh PNG."""
    if not prompts_file.exists():
        return []

    content = prompts_file.read_text(encoding="utf-8")
    tasks = []

    for line in content.splitlines():
        line = line.strip()
        if not line.startswith("|") or not line.endswith("|"):
            continue

        parts = [p.strip() for p in line.split("|")]
        # Header or separator
        if len(parts) < 4:
            continue

        assigned_acc = None
        if len(parts) >= 6 and "Account" in parts[1]:
            acc_raw = parts[1].replace("*", "").replace("Account", "").strip()
            if acc_raw.isdigit():
                assigned_acc = int(acc_raw)
            col1 = parts[4].strip("` ")
            prompt_col = parts[5]
        else:
            col1 = parts[1].strip("` ")
            prompt_col = parts[2]

        if col1.endswith(".png") and not prompt_col.startswith("**[20/20"):
            # Scene id e.g. S001 from S001-A_6s_AIV_sb.png
            scene_id = col1.split("-")[0].split("_")[0]
            # Alias file e.g. scene_01.png
            try:
                num = int(scene_id.replace("S", ""))
                alias_file = f"scene_{num:02d}.png"
            except Exception:
                alias_file = f"{scene_id}.png"

            tasks.append({
                "target_file": col1,
                "alias_file": alias_file,
                "scene_id": scene_id,
                "prompt": prompt_col,
                "assigned_acc": assigned_acc
            })

    return tasks


def execute_single_task(task, acc_id, port, assets_dir: Path):
    scene_id = task["scene_id"]
    target_file = task["target_file"]
    prompt = task["prompt"]

    print(f"\n[Account {acc_id} | Port {port}] ▶ Bắt đầu xử lý {scene_id} ({target_file})...")
    client = FlowCDPClient(port=port, acc_id=acc_id)

    try:
        client.connect()
        print(f"  🔗 [Account {acc_id}] Đã kết nối WebSocket CDP thành công.")

        baseline = client.get_existing_image_urls()
        print(f"  📸 [Account {acc_id}] Đã ghi nhận baseline ({len(baseline)} ảnh hiện có trên trang).")

        print(f"  ✍️ [Account {acc_id}] Điền prompt vào .ProseMirror và gửi phím Enter...")
        client.inject_and_submit_prompt(prompt)
        print(f"  🚀 [Account {acc_id}] Đã gửi prompt! Đang chờ Google Flow tạo ảnh...")

        new_image_url = client.poll_for_new_image(baseline, timeout=140)
        if new_image_url:
            print(f"  ✨ [Account {acc_id}] Phát hiện ảnh mới: {new_image_url[:65]}...")
            print(f"  📥 [Account {acc_id}] Đang tải bytes ảnh qua browser fetch() session...")
            img_bytes = client.fetch_image_bytes_in_browser(new_image_url)

            if img_bytes:
                target_path = assets_dir / target_file
                target_path.write_bytes(img_bytes)

                sz = len(img_bytes) // 1024
                print(f"  💾 [Account {acc_id}] ĐÃ LƯU THÀNH CÔNG: {target_file} ({sz} KB)")
                return {"acc_id": acc_id, "scene_id": scene_id, "success": True, "file": target_file}
            else:
                print(f"  ⚠️ [Account {acc_id}] Lỗi giải mã bytes ảnh từ browser fetch")
        else:
            print(f"  ⚠️ [Account {acc_id}] Hết timeout (140s), chưa nhận được URL ảnh mới")

    except Exception as e:
        print(f"  ❌ [Account {acc_id}] Lỗi xử lý: {e}")
    finally:
        client.close()

    return {"acc_id": acc_id, "scene_id": scene_id, "success": False, "file": target_file}


def update_composition_files(assets_dir: Path, tasks):
    """Cập nhật các file ảnh vừa tải vào remotion-composition.json."""
    comp_file = assets_dir / "remotion-composition.json"
    if not comp_file.exists():
        return

    try:
        data = json.loads(comp_file.read_text(encoding="utf-8"))
        seqs = data.get("tracks", {}).get("visual_sequences", [])
        updated_count = 0

        for t in tasks:
            target_file = t["target_file"]
            local_path = assets_dir / target_file
            if local_path.exists():
                for seq in seqs:
                    if seq.get("scene_id") == t["scene_id"] and seq.get("id", "").startswith(t["scene_id"]):
                        seq["component"] = "KenBurnsImage"
                        seq["props"] = {
                            "src": f"assets/{target_file}",
                            "animation": "pan-right" if int(t["scene_id"].replace("S", "") or "1") % 2 == 1 else "zoom-in"
                        }
                        updated_count += 1
                        break

        comp_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\n🎬 Đã cập nhật {updated_count} cảnh trong remotion-composition.json!")
    except Exception as e:
        print(f"⚠️ Lỗi cập nhật remotion-composition.json: {e}")


def run_wave(wave_tasks, assets_dir: Path):
    """Chạy song song 1 batch qua tối đa 5 account."""
    print("=" * 76)
    print(f"🚀 BẮT ĐẦU CHẠY BATCH ({len(wave_tasks)} tác vụ) QUA {len(wave_tasks)} TÀI KHOẢN GOOGLE FLOW CDP")
    print("=" * 76)

    start_time = time.time()
    results = []

    with ThreadPoolExecutor(max_workers=len(wave_tasks)) as executor:
        futures = []
        for idx, task in enumerate(wave_tasks):
            acc_id = task.get("assigned_acc") or (idx + 1)
            port = ACCOUNT_PORTS[acc_id]
            futures.append(executor.submit(execute_single_task, task, acc_id, port, assets_dir))

        for f in futures:
            results.append(f.result())

    elapsed = int(time.time() - start_time)
    update_composition_files(assets_dir, wave_tasks)

    successes = [r for r in results if r["success"]]
    print("\n" + "=" * 76)
    print(f"🎉 KẾT QUẢ BATCH ({len(successes)}/{len(wave_tasks)} thành công, tổng thời gian: {elapsed}s):")
    for r in results:
        status_icon = "✅" if r["success"] else "❌"
        print(f"   {status_icon} Account {r['acc_id']}: {r['scene_id']} -> {r['file']}")
    print("=" * 76)
    return successes


def trigger_auto_qa(channel: str, slug: str, dry_run: bool = False):
    """Tự động kích hoạt QA verifier và render video khi assets hoàn tất 100%."""
    qa_script = ROOT_DIR / "tools" / "qa" / "auto_qa_trigger.py"
    if not qa_script.exists():
        print(f"⚠️ Không tìm thấy script QA tại: {qa_script}")
        return
    print("\n" + "=" * 76)
    print("⚡ [AUTO-TRIGGER HOOK] TẤT CẢ ASSETS ĐÃ HOÀN TẤT (100%) -> TỰ ĐỘNG CHẠY QA PIPELINE!")
    print("=" * 76)
    cmd = [sys.executable, str(qa_script), slug, "--channel", channel]
    if dry_run:
        cmd.append("--dry-run")
    subprocess.run(cmd, cwd=str(ROOT_DIR))


def main():
    parser = argparse.ArgumentParser(description="Google Flow Multi-Account Batch Dispatcher")
    parser.add_argument("--channel", default="tien-thuc-chien", help="Channel slug")
    parser.add_argument("--slug", default="thoat-bay-no-the-tin-dung", help="Video slug")
    parser.add_argument("--status", action="store_true", help="Hiển thị thống kê tiến độ")
    parser.add_argument("--wave", type=int, default=0, help="Chạy một wave cụ thể (1, 2, 3...)")
    parser.add_argument("--auto", action="store_true", help="Chạy tự động liên tục các wave còn thiếu")
    parser.add_argument("--batch-size", type=int, default=5, help="Số cảnh mỗi batch (mặc định 5)")
    parser.add_argument("--no-qa", action="store_true", help="Tắt auto-trigger QA khi hoàn tất")
    parser.add_argument("--dry-run-qa", action="store_true", help="Chạy giả lập QA/render không render thực tế")
    args = parser.parse_args()

    video_dir = ROOT_DIR / "channels" / args.channel / "videos" / args.slug
    assets_dir = video_dir / "assets"
    prompts_file = assets_dir / "prompts.md"

    if not prompts_file.exists():
        print(f"❌ Không tìm thấy prompts.md tại {prompts_file}")
        sys.exit(1)

    all_tasks = parse_prompts_file(prompts_file)
    existing_files = {f.name for f in assets_dir.glob("*.png")}

    completed_tasks = [t for t in all_tasks if t["target_file"] in existing_files]
    missing_tasks = [t for t in all_tasks if t["target_file"] not in existing_files]

    print("=" * 76)
    print(f"📊 TIẾN ĐỘ ASSETS: {args.slug} ({args.channel})")
    print(f"   • Tổng số cảnh PNG cần tạo: {len(all_tasks)}")
    print(f"   • Đã hoàn tất: {len(completed_tasks)} ({len(completed_tasks)*100//len(all_tasks) if all_tasks else 0}%)")
    print(f"   • Còn thiếu: {len(missing_tasks)}")
    print("=" * 76)

    if args.status:
        if missing_tasks:
            print("\n📋 Danh sách các cảnh tiếp theo cần tạo:")
            for idx, t in enumerate(missing_tasks[:15], 1):
                print(f"   {idx:02d}. {t['scene_id']} -> {t['target_file']}")
            if len(missing_tasks) > 15:
                print(f"   ... và {len(missing_tasks) - 15} cảnh khác.")
        else:
            print("🎉 TẤT CẢ CÁC CẢNH ẢNH PNG ĐÃ ĐƯỢC TẠO HOÀN TẤT!")
        return

    if args.wave > 0:
        # Chạy cụ thể Wave N
        wave_idx = args.wave
        # Mỗi wave có batch_size
        start_idx = (wave_idx - 1) * args.batch_size
        end_idx = start_idx + args.batch_size
        selected = all_tasks[start_idx:end_idx]
        if not selected:
            print(f"⚠️ Wave {wave_idx} không có cảnh nào (ngoài phạm vi {len(all_tasks)} cảnh)!")
            return

        # Lọc bỏ các cảnh đã có trừ khi user muốn tạo lại
        to_run = [t for t in selected if t["target_file"] not in existing_files]
        if not to_run:
            print(f"✅ Tất cả {len(selected)} cảnh trong Wave {wave_idx} đã có sẵn!")
            return

        run_wave(to_run, assets_dir)
        return

    if args.auto:
        # Chạy tự động tất cả các cảnh còn thiếu theo từng batch 5
        wave_count = 1
        failed_attempts = {}
        while missing_tasks:
            runnable = [t for t in missing_tasks if failed_attempts.get(t["target_file"], 0) < 3]
            if not runnable:
                print("⚠️ Các cảnh còn lại đều đã thử quá 3 lần. Dừng để kiểm tra.")
                break

            # Đảm bảo mỗi tài khoản chỉ nhận tối đa 1 task trong cùng 1 batch để tránh xung đột CDP
            current_batch = []
            used_accs = set()
            for t in runnable:
                acc = t.get("assigned_acc") or 1
                if acc not in used_accs:
                    current_batch.append(t)
                    used_accs.add(acc)
                    if len(current_batch) >= args.batch_size:
                        break

            if not current_batch:
                current_batch = runnable[:args.batch_size]
            print(f"\n⚡ ĐANG THỰC THI BATCH TỰ ĐỘNG #{wave_count} ({len(current_batch)} CẢNH)...")
            run_wave(current_batch, assets_dir)

            # Cập nhật số lần fail nếu chưa tải được
            existing_files = {f.name for f in assets_dir.glob("*.png")}
            for t in current_batch:
                if t["target_file"] not in existing_files:
                    failed_attempts[t["target_file"]] = failed_attempts.get(t["target_file"], 0) + 1

            missing_tasks = [t for t in all_tasks if t["target_file"] not in existing_files]
            wave_count += 1

            if missing_tasks and any(failed_attempts.get(t["target_file"], 0) < 3 for t in missing_tasks):
                print("⏳ Nghỉ 5s trước khi chuyển batch tiếp theo...")
                time.sleep(5)

        if not missing_tasks:
            print("\n🎉🎉 CHÚC MỪNG: TẤT CẢ CÁC CẢNH ĐÃ ĐƯỢC DISPATCH VÀ TẢI VỀ THÀNH CÔNG! 🎉🎉")
            if not args.no_qa:
                trigger_auto_qa(args.channel, args.slug, dry_run=args.dry_run_qa)
        return

    # Nếu không chỉ định args, mặc định chạy batch tiếp theo của missing_tasks
    if missing_tasks:
        next_batch = missing_tasks[:args.batch_size]
        print(f"\n🚀 Tự động chạy batch 5 cảnh tiếp theo ({len(next_batch)} cảnh)...")
        run_wave(next_batch, assets_dir)
        remaining = [t for t in all_tasks if t["target_file"] not in {f.name for f in assets_dir.glob("*.png")}]
        if not remaining:
            print("\n🎉🎉 TẤT CẢ CÁC CẢNH ĐÃ HOÀN TẤT 100%!")
            if not args.no_qa:
                trigger_auto_qa(args.channel, args.slug, dry_run=args.dry_run_qa)
    else:
        print("✅ Tất cả các cảnh đã hoàn tất 100%!")
        if not args.no_qa:
            trigger_auto_qa(args.channel, args.slug, dry_run=args.dry_run_qa)


if __name__ == "__main__":
    main()
