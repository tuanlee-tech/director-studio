#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
storyboard_to_aiv.py — Google Flow Storyboard-to-Video (AIV) Auto-Dispatcher (CDP)
Hỗ trợ đầy đủ song ngữ Anh - Việt (EN & VI UI) trên 5 tài khoản Google Flow CDP:
  • Acc 1 (9223): S001-A_6s_AIV.mp4
  • Acc 2 (9224): S002-A_6s_AIV.mp4
  • Acc 3 (9225): S003-A_6s_AIV.mp4
  • Acc 4 (9226): S004-A_6s_AIV.mp4
  • Acc 5 (9227): S064-A_6s_AIV.mp4
"""

import sys
import os
import json
import time
import shutil
import subprocess
import urllib.request
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
CHANNEL = "tien-thuc-chien"
SLUG = "thoat-bay-no-the-tin-dung"
VIDEO_DIR = ROOT_DIR / "channels" / CHANNEL / "videos" / SLUG
ASSETS_DIR = VIDEO_DIR / "assets"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)
DOWNLOADS_DIR = Path.home() / "Downloads"

try:
    import websocket
except ImportError:
    print("❌ Thiếu websocket-client.")
    sys.exit(1)


STORYBOARD_TASKS = [
    {
        "acc_id": 1,
        "port": 9223,
        "scene_id": "S001",
        "sb_pattern": r"phone alert|man reacting|shock|nợ 40 triệu",
        "output_file": "S001-A_6s_AIV.mp4",
        "prompt": "Use the attached storyboard image as the shot plan: animate panel 1 through panel 3 in order, with the timings below, as ONE continuous full-frame 6-second shot. Do not show panel borders, a grid or multiple panels. The young man starts smiling looking at his phone, his smile quickly freezes and fades, his eyes widen in extreme comic shock, mouth opens in disbelief, sweat drops appear on his forehead as a red downward arrow icon floats beside him. Audio: only natural ambient sound and scene sound effects; no music, no speech, no dialogue, no singing, no narration; characters never speak and keep their mouths closed. 2D flat vector cartoon illustration, Vyond animation style, thick black outlines, vibrant and highly saturated solid colors. Flat shading, no complex lighting. White background. Expressive characters with exaggerated comic-style facial expressions (shock, anger, confidence). Incorporate floating financial icons like gold coins, credit cards, or red downward arrows. High contrast, clean composition. No 3D rendering, no CGI, no photorealism. Avoid: Photorealism, 3D render, CGI, text, letters, typography, watermarks, signature, distorted faces, dark lighting, complex gradients."
    },
    {
        "acc_id": 2,
        "port": 9224,
        "scene_id": "S002",
        "sb_pattern": r"paying with credit card|pos|receipt|lounge|quẹt thẻ",
        "output_file": "S002-A_6s_AIV.mp4",
        "prompt": "Use the attached storyboard image as the shot plan: animate panel 1 through panel 4 in order, with the timings below, as ONE continuous full-frame 8-second shot. Do not show panel borders, a grid or multiple panels. The young man proudly presents the card, swipes it across the terminal, a receipt scrolls out rapidly, and his confident expression softens into an uneasy hesitation. Audio: only natural ambient sound and scene sound effects; no music, no speech, no dialogue, no singing, no narration; characters never speak and keep their mouths closed. 2D flat vector cartoon illustration, Vyond animation style, thick black outlines, vibrant and highly saturated solid colors. Flat shading, no complex lighting. White background. Expressive characters with exaggerated comic-style facial expressions (shock, anger, confidence). Incorporate floating financial icons like gold coins, credit cards, or red downward arrows. High contrast, clean composition. No 3D rendering, no CGI, no photorealism. Avoid: Photorealism, 3D render, CGI, text, letters, typography, watermarks, signature, distorted faces, dark lighting, complex gradients."
    },
    {
        "acc_id": 3,
        "port": 9225,
        "scene_id": "S003",
        "sb_pattern": r"wallet sinking|ocean abyss|underwater|chìm",
        "output_file": "S003-A_6s_AIV.mp4",
        "prompt": "Use the attached storyboard image as the shot plan: animate panel 1 through panel 4 in order, with the timings below, as ONE continuous full-frame 8-second shot. Do not show panel borders, a grid or multiple panels. The floating wallet is snagged by the heavy iron anchor, which drags it underwater with accelerating downward motion, leaving a trail of rising bubbles. Audio: only natural ambient sound and scene sound effects; no music, no speech, no dialogue, no singing, no narration; characters never speak and keep their mouths closed. 2D flat vector cartoon illustration, Vyond animation style, thick black outlines, vibrant and highly saturated solid colors. Flat shading, no complex lighting. White background. Expressive characters with exaggerated comic-style facial expressions (shock, anger, confidence). Incorporate floating financial icons like gold coins, credit cards, or red downward arrows. High contrast, clean composition. No 3D rendering, no CGI, no photorealism. Avoid: Photorealism, 3D render, CGI, text, letters, typography, watermarks, signature, distorted faces, dark lighting, complex gradients."
    },
    {
        "acc_id": 4,
        "port": 9226,
        "scene_id": "S004",
        "sb_pattern": r"parting mist|host|studio backdrop|sương mù",
        "output_file": "S004-A_6s_AIV.mp4",
        "prompt": "Use the attached storyboard image as the shot plan: animate panel 1 through panel 4 in order, with the timings below, as ONE continuous full-frame 8-second shot. Do not show panel borders, a grid or multiple panels. The host steps through the dissipating fog, smiles warmly and confidently at the camera, and raises an open hand as four green numbered badges pop up with a playful bounce. Audio: only natural ambient sound and scene sound effects; no music, no speech, no dialogue, no singing, no narration; characters never speak and keep their mouths closed. 2D flat vector cartoon illustration, Vyond animation style, thick black outlines, vibrant and highly saturated solid colors. Flat shading, no complex lighting. White background. Expressive characters with exaggerated comic-style facial expressions (shock, anger, confidence). Incorporate floating financial icons like gold coins, credit cards, or red downward arrows. High contrast, clean composition. No 3D rendering, no CGI, no photorealism. Avoid: Photorealism, 3D render, CGI, text, letters, typography, watermarks, signature, distorted faces, dark lighting, complex gradients."
    },
    {
        "acc_id": 5,
        "port": 9227,
        "scene_id": "S064",
        "sb_pattern": r"scissors cutting credit card|scissors|cắt thẻ",
        "output_file": "S064-A_6s_AIV.mp4",
        "prompt": "Use the attached storyboard image as the shot plan: animate panel 1 through panel 3 in order, with the timings below, as ONE continuous full-frame 6-second shot. Do not show panel borders, a grid or multiple panels. The scissors cleanly snip through the plastic credit card with a decisive motion, the two halves spring slightly apart and settle onto the surface as sparkling light bursts forth. Audio: only natural ambient sound and scene sound effects; no music, no speech, no dialogue, no singing, no narration; characters never speak and keep their mouths closed. 2D flat vector cartoon illustration, Vyond animation style, thick black outlines, vibrant and highly saturated solid colors. Flat shading, no complex lighting. White background. Expressive characters with exaggerated comic-style facial expressions (shock, anger, confidence). Incorporate floating financial icons like gold coins, credit cards, or red downward arrows. High contrast, clean composition. No 3D rendering, no CGI, no photorealism. Avoid: Photorealism, 3D render, CGI, text, letters, typography, watermarks, signature, distorted faces, dark lighting, complex gradients."
    }
]


class FlowVideoCDPClient:
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
        while time.time() - start < 20:
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

    def is_generation_running(self):
        js = """(() => {
            const stopBtn = document.querySelector('button[aria-label*="Stop" i], button[aria-label*="Cancel" i], button[aria-label*="Dừng" i], button[aria-label*="Hủy" i]');
            return stopBtn !== null && stopBtn.offsetParent !== null;
        })()"""
        return bool(self.evaluate(js))

    def trigger_animate_for_storyboard(self, pattern_str):
        escaped_pat = json.dumps(pattern_str)
        js = f"""(() => {{
            const pat = new RegExp({escaped_pat}, 'i');
            const tiles = Array.from(document.querySelectorAll('flow-grid-tile-container'));
            const tile = tiles.find(t => pat.test(t.innerText) || pat.test(t.getAttribute('aria-label') || '') || pat.test(t.querySelector('button[aria-haspopup="true"]')?.getAttribute('aria-label') || ''));
            if (!tile) return {{ success: false, error: 'Không tìm thấy tile storyboard phù hợp' }};

            // Tìm nút More options (EN hoặc VI)
            const moreBtn = tile.querySelector('button[aria-label*="options" i], button[aria-label*="khác" i], button[aria-label="More options"]');
            if (!moreBtn) return {{ success: false, error: 'Nút More options không tồn tại trên tile' }};
            moreBtn.click();
            return {{ success: true, tileText: tile.innerText.slice(0, 40) }};
        }})()"""
        r1 = self.evaluate(js)
        if not r1 or not r1.get("success"):
            return r1

        time.sleep(0.4)

        js_click_animate = """(() => {
            const items = Array.from(document.querySelectorAll('.mat-mdc-menu-item, [role="menuitem"]'));
            const btn = items.find(it => /animate|tạo ảnh động/i.test(it.innerText) || it.innerText.includes('motion_blur'));
            if (!btn) return { success: false, error: 'Không tìm thấy Animate / Tạo ảnh động trong menu' };
            btn.click();
            return { success: true };
        })()"""
        return self.evaluate(js_click_animate)

    def inject_and_submit_prompt(self, prompt_text):
        escaped = json.dumps(prompt_text)
        js = f"""(() => {{
            const el = document.querySelector('.ProseMirror');
            if (!el) return {{ success: false, error: 'Không tìm thấy ProseMirror' }};
            el.focus();
            document.execCommand('selectAll', false, null);
            document.execCommand('insertText', false, {escaped});
            el.dispatchEvent(new InputEvent('input', {{ bubbles: true }}));
            return {{ success: true }};
        }})()"""
        r = self.evaluate(js)
        if not r or not r.get("success"):
            raise RuntimeError(f"Không thể nhập prompt: {r}")

        time.sleep(0.5)

        self.send_cdp("Input.dispatchKeyEvent", {
            "type": "rawKeyDown", "windowsVirtualKeyCode": 13, "unmodifiedText": "\r", "text": "\r", "key": "Enter", "code": "Enter"
        })
        self.send_cdp("Input.dispatchKeyEvent", {
            "type": "keyUp", "windowsVirtualKeyCode": 13, "unmodifiedText": "\r", "text": "\r", "key": "Enter", "code": "Enter"
        })
        return True

    def poll_for_video_ready(self, timeout=360):
        """Giám sát tile video cho đến khi hoàn tất 100%."""
        start = time.time()
        time.sleep(8)  # Đợi 8s ban đầu để tile video mount chắc chắn

        while time.time() - start < timeout:
            js_status = """(() => {
                const videoTile = document.querySelector('flow-video-tile');
                if (!videoTile) return { found: false, ready: false };
                
                const text = videoTile.innerText;
                // Kiểm tra xem còn tiến trình % không
                const hasProgress = /\\b\\d+%/i.test(text);
                return {
                    found: true,
                    text: text.slice(0, 60),
                    ready: !hasProgress && (text.includes('play_circle') || !!videoTile.querySelector('img, video'))
                };
            })()"""
            st = self.evaluate(js_status) or {}
            if st.get("found") and st.get("ready"):
                return True

            time.sleep(4)

        return False

    def trigger_download_720p(self):
        """Bấm More options -> Hover Download -> Click 720p Original size."""
        # 1. Mở More options
        js_more = """(() => {
            const moreBtn = document.querySelector('flow-video-tile button[aria-label*="options" i], flow-video-tile button[aria-label*="khác" i], flow-video-tile button[aria-label="More options"]');
            if (moreBtn) moreBtn.click();
            return !!moreBtn;
        })()"""
        self.evaluate(js_more)
        time.sleep(0.4)

        # 2. Hover Download / Tải xuống
        js_hover = """(() => {
            const items = Array.from(document.querySelectorAll('.mat-mdc-menu-item'));
            const dl = items.find(b => /download|tải xuống/i.test(b.innerText));
            if (dl) {
                dl.dispatchEvent(new MouseEvent('mouseenter', { bubbles: true }));
                dl.click();
                return true;
            }
            return false;
        })()"""
        self.evaluate(js_hover)
        time.sleep(0.5)

        # 3. Click 720p / Kích thước gốc
        js_click_720 = """(() => {
            const btns = Array.from(document.querySelectorAll('.mat-mdc-menu-item, button'));
            const opt = btns.find(b => /720p/i.test(b.innerText) || /original size|kích thước gốc/i.test(b.innerText));
            if (opt) {
                opt.click();
                return true;
            }
            return false;
        })()"""
        return bool(self.evaluate(js_click_720))


def execute_storyboard_to_aiv(task):
    acc_id = task["acc_id"]
    port = task["port"]
    scene_id = task["scene_id"]
    output_file = task["output_file"]
    sb_pattern = task["sb_pattern"]
    prompt = task["prompt"]
    target_path = ASSETS_DIR / output_file

    # Nếu đã có file thì bỏ qua
    if target_path.exists() and target_path.stat().st_size > 500000:
        print(f"\n[Account {acc_id} | Port {port}] ✅ {output_file} đã có sẵn ({target_path.stat().st_size // 1024} KB), bỏ qua.")
        return {"acc_id": acc_id, "scene_id": scene_id, "success": True, "file": output_file}

    print(f"\n[Account {acc_id} | Port {port}] ▶ Khởi chạy Storyboard -> AIV cho {scene_id} ({output_file})...")
    client = FlowVideoCDPClient(port=port, acc_id=acc_id)

    try:
        client.connect()
        print(f"  🔗 [Account {acc_id}] Kết nối CDP thành công.")

        # Kiểm tra xem có flow-video-tile đang tồn tại không
        js_tile_check = """(() => {
            const vt = document.querySelector('flow-video-tile');
            return vt ? { exists: true, text: vt.innerText.slice(0, 60) } : { exists: false };
        })()"""
        tc = client.evaluate(js_tile_check) or {}

        if tc.get("exists") and "%" not in tc.get("text", ""):
            print(f"  ✨ [Account {acc_id}] Video tile đã sinh xong sẵn trên trang! Bắt đầu tải file...")
        elif tc.get("exists") and "%" in tc.get("text", ""):
            print(f"  ⏳ [Account {acc_id}] Video tile đang trong tiến trình sinh ({tc.get('text')}), tiếp tục đợi...")
            ready = client.poll_for_video_ready(timeout=360)
            if not ready:
                raise RuntimeError("Hết timeout chờ video hoàn tất")
        else:
            # Chưa có video tile -> Tìm Storyboard và bấm Animate
            print(f"  🎯 [Account {acc_id}] Định vị tile Storyboard ({sb_pattern})...")
            r_anim = client.trigger_animate_for_storyboard(sb_pattern)
            if not r_anim or not r_anim.get("success"):
                raise RuntimeError(f"Lỗi kích hoạt Animate: {r_anim}")

            print(f"  ✨ [Account {acc_id}] Đã bấm 'Animate'! Đợi đính kèm ingredient...")
            time.sleep(1.2)

            print(f"  ✍️ [Account {acc_id}] Điền prompt AIV và gửi phím Enter...")
            client.inject_and_submit_prompt(prompt)
            print(f"  🚀 [Account {acc_id}] Đã gửi lệnh! Đang sinh video AIV...")

            ready = client.poll_for_video_ready(timeout=360)
            if not ready:
                raise RuntimeError("Hết timeout chờ video hoàn tất")

        # Video đã sẵn sàng -> Bấm Download 720p
        print(f"  📥 [Account {acc_id}] Kích hoạt Download 720p qua Google Flow UI...")
        before_files = set(f.name for f in DOWNLOADS_DIR.glob("*.mp4"))

        ok_dl = client.trigger_download_720p()
        if not ok_dl:
            print(f"  ⚠️ [Account {acc_id}] Thử bấm download lần 2...")
            time.sleep(1)
            client.trigger_download_720p()

        # Đợi file tải về ~/Downloads
        for _ in range(25):
            time.sleep(1)
            after_files = set(f.name for f in DOWNLOADS_DIR.glob("*.mp4"))
            diff = after_files - before_files
            if diff:
                dl_file = list(diff)[0]
                shutil.copyfile(DOWNLOADS_DIR / dl_file, target_path)
                sz_kb = target_path.stat().st_size // 1024
                print(f"  💾 [Account {acc_id}] ĐÃ LƯU THÀNH CÔNG: {output_file} ({sz_kb} KB)")
                return {"acc_id": acc_id, "scene_id": scene_id, "success": True, "file": output_file}

        # Fallback kiểm tra file mới nhất trong Downloads (trong 60s gần nhất)
        recent = [f for f in DOWNLOADS_DIR.glob("*.mp4") if time.time() - f.stat().st_mtime < 60]
        if recent:
            latest = max(recent, key=lambda f: f.stat().st_mtime)
            shutil.copyfile(latest, target_path)
            sz_kb = target_path.stat().st_size // 1024
            print(f"  💾 [Account {acc_id}] ĐÃ LƯU THÀNH CÔNG (từ Downloads): {output_file} ({sz_kb} KB)")
            return {"acc_id": acc_id, "scene_id": scene_id, "success": True, "file": output_file}

        raise RuntimeError("Không tìm thấy file MP4 sau khi bấm download")

    except Exception as e:
        print(f"  ❌ [Account {acc_id}] Lỗi: {e}")
    finally:
        client.close()

    return {"acc_id": acc_id, "scene_id": scene_id, "success": False, "file": output_file}


def update_composition_aiv():
    comp_file = ASSETS_DIR / "remotion-composition.json"
    if not comp_file.exists():
        return
    try:
        data = json.loads(comp_file.read_text(encoding="utf-8"))
        seqs = data.get("tracks", {}).get("visual_sequences", [])
        updated = 0
        for t in STORYBOARD_TASKS:
            out_file = t["output_file"]
            p = ASSETS_DIR / out_file
            if p.exists():
                for seq in seqs:
                    if seq.get("scene_id") == t["scene_id"] and seq.get("id", "").startswith(t["scene_id"]):
                        seq["type"] = "AIV"
                        seq["component"] = "Video"
                        seq["props"] = {"src": f"assets/{out_file}"}
                        updated += 1
                        break
        comp_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\n🎬 Đã cập nhật {updated} cảnh AIV Video vào remotion-composition.json!")
    except Exception as e:
        print(f"⚠️ Lỗi cập nhật remotion: {e}")


def main():
    print("=" * 76)
    print("🎬 CHUYỂN ĐỔI STORYBOARD -> AI VIDEO (AIV) TRÊN 5 TÀI KHOẢN GOOGLE FLOW CDP")
    print(f"   Dự án: {SLUG} | Cảnh: S001, S002, S003, S004, S064")
    print("=" * 76)

    start_time = time.time()
    results = []

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(execute_storyboard_to_aiv, task) for task in STORYBOARD_TASKS]
        for f in futures:
            results.append(f.result())

    elapsed = int(time.time() - start_time)
    update_composition_aiv()

    successes = [r for r in results if r["success"]]
    print("\n" + "=" * 76)
    print(f"🎉 HOÀN TẤT AIV DISPATCH ({len(successes)}/5 thành công, thời gian: {elapsed}s):")
    for r in results:
        icon = "✅" if r["success"] else "❌"
        print(f"   {icon} Account {r['acc_id']}: {r['scene_id']} -> {r['file']}")
    print("=" * 76)

    # Auto-trigger QA pipeline khi hoàn tất toàn bộ AIV
    qa_script = ROOT_DIR / "tools" / "qa" / "auto_qa_trigger.py"
    if qa_script.exists():
        print("\n" + "=" * 76)
        print("⚡ [AUTO-TRIGGER HOOK] AIV HOÀN TẤT -> TỰ ĐỘNG KÍCH HOẠT QA PIPELINE!")
        print("=" * 76)
        subprocess.run([sys.executable, str(qa_script), SLUG, "--channel", CHANNEL], cwd=str(ROOT_DIR))


if __name__ == "__main__":
    main()
