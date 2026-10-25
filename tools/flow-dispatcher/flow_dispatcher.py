#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
flow_dispatcher.py — Google Flow Multi-Account Batch Dispatcher
Điều phối tự động phân chia prompt video cho 5 tài khoản Google Flow qua CDP.
Thực hiện 4 bước CDP:
1. Kết nối Chrome CDP
2. Điều hướng tới Google Flow Project
3. Nhập prompt vào ProseMirror và Enter đúng 1 lần
4. Poll spinner/tiles và sync media về Studio + follow-up sync (+10s, +20s, +30s)
"""

import sys
import os
import json
import time
import re
import argparse
import threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# Fix UTF-8 console output for Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent.parent
CONFIG_FILE = SCRIPT_DIR / "accounts.json"

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from browser_pool import load_accounts_config, check_cdp_status, get_active_tabs
from browser_flow import FlowBrowserSession, sync_flow_media_to_studio


def resolve_active_video(root_dir, channel=None, slug=None):
    channels_dir = root_dir / "channels"
    active_channel = channel

    if slug and not active_channel and channels_dir.exists():
        for c in channels_dir.iterdir():
            if c.is_dir() and (c / "videos" / slug).exists():
                active_channel = c.name
                break

    if not active_channel:
        cfg_file = root_dir / ".agents" / "skills" / "video-director" / "resources" / "config.json"
        if cfg_file.exists():
            try:
                cfg = json.loads(cfg_file.read_text(encoding="utf-8"))
                val = cfg.get("active_channel")
                if val:
                    active_channel = val
            except Exception:
                pass

    if not active_channel and channels_dir.exists():
        for c in channels_dir.iterdir():
            if c.is_dir() and not c.name.startswith("."):
                active_channel = c.name
                break

    if not active_channel:
        active_channel = "tien-thuc-chien"

    ch_dir = channels_dir / active_channel
    if not slug:
        videos_dir = ch_dir / "videos"
        if videos_dir.exists():
            for v in videos_dir.iterdir():
                if v.is_dir() and not v.name.startswith("."):
                    slug = v.name
                    break

    if not slug:
        slug = "thoat-bay-no-the-tin-dung"

    return active_channel, slug


def load_video_prompts(root_dir, channel, slug):
    """Đọc danh sách B-roll và prompts từ broll-plan.json hoặc remotion-composition.json."""
    video_dir = root_dir / "channels" / channel / "videos" / slug
    comp_file = video_dir / "assets" / "remotion-composition.json"
    broll_file = video_dir / "broll-plan.json"

    items = []
    if comp_file.exists():
        try:
            data = json.loads(comp_file.read_text(encoding="utf-8"))
            scenes = data.get("scenes", [])
            for s in scenes:
                items.append({
                    "id": f"Scene-{s.get('index', 1)}",
                    "scene": f"Scene {s.get('index', 1)}",
                    "index": s.get("index", 1),
                    "type": "AIV" if s.get("broll_type") == "AIV" else "IMG",
                    "duration": s.get("duration", 4),
                    "beat": s.get("visual_beat", ""),
                    "target_file": f"scene_{s.get('index', 1):02d}.png",
                    "prompt": s.get("prompt") or f"{s.get('visual_beat')}, 2D flat vector cartoon style, finance illustration"
                })
            if items:
                return items
        except Exception:
            pass

    if broll_file.exists():
        try:
            data = json.loads(broll_file.read_text(encoding="utf-8"))
            for idx, b in enumerate(data, start=1):
                items.append({
                    "id": b.get("broll_id", f"S{idx:03d}-A"),
                    "scene": b.get("scene", f"Scene {idx}"),
                    "index": idx,
                    "type": b.get("type", "AIV"),
                    "duration": b.get("duration_seconds", 4),
                    "beat": b.get("visual_beat", ""),
                    "target_file": f"{b.get('broll_id')}_{b.get('type')}.{'mp4' if b.get('type') == 'AIV' else 'png'}",
                    "prompt": f"{b.get('visual_beat')}, 2D flat vector cartoon style, highly detailed 8k"
                })
            return items
        except Exception:
            pass

    # Mock default nếu chưa có broll plan
    return [
        {"id": "Scene-1", "scene": "Scene 1", "index": 1, "type": "AIV", "duration": 6, "target_file": "scene_01.mp4", "prompt": "Man looking shocked at red credit card bill, 2D vector style"},
        {"id": "Scene-2", "scene": "Scene 2", "index": 2, "type": "AIV", "duration": 4, "target_file": "scene_02.mp4", "prompt": "Salary notification arrives on phone, 2D vector style"},
        {"id": "Scene-3", "scene": "Scene 3", "index": 3, "type": "IMG", "duration": 4, "target_file": "scene_03.png", "prompt": "Credit card cut in half with scissors on table, 2D vector style"},
        {"id": "Scene-4", "scene": "Scene 4", "index": 4, "type": "IMG", "duration": 4, "target_file": "scene_04.png", "prompt": "Financial freedom roadmap with green upward chart, 2D vector style"}
    ]


def schedule_followup_sync(session, channel, slug, scene_idx, scene_label, is_video):
    """
    Follow-up sync ở +10s / +20s / +30s đề phòng trường hợp Flow render trễ.
    """
    def _delayed_check():
        for delay in [10, 20, 30]:
            time.sleep(delay)
            try:
                st = session.poll_tiles_status([scene_label])
                for t in st.get("tiles", []):
                    if scene_label.lower() in (t.get("title") or "").lower() and t.get("media_url") and not t.get("in_progress"):
                        sync_flow_media_to_studio(channel, slug, scene_idx, t["media_url"], is_video=is_video)
                        print(f"✨ [Follow-up +{delay}s] Đã sync trễ thành công cho {scene_label}!")
                        return
            except Exception:
                pass

    threading.Thread(target=_delayed_check, daemon=True).start()


def dispatch_worker(acc_info, batch_items, channel, slug, dry_run=False):
    """Worker xử lý batch prompts cho 1 tài khoản Chrome."""
    acc_id = acc_info["id"]
    port = acc_info["port"]
    name = acc_info["name"]
    project_url = acc_info.get("project_url")

    print(f"\n[Account {acc_id} - {name}] Bắt đầu xử lý {len(batch_items)} items...")

    if dry_run:
        for it in batch_items:
            print(f"  👉 [Account {acc_id}] Mock dispatch: {it['id']} ({it['type']}) → {it['target_file']}")
            time.sleep(0.5)
        return len(batch_items), 0

    session = FlowBrowserSession(port=port, project_url=project_url)
    success_count = 0
    fail_count = 0

    try:
        session.connect()
        print(f"  🔗 [Account {acc_id}] Đã kết nối Flow tab: {session.tab_url}")

        for it in batch_items:
            prompt_text = it["prompt"]
            scene_label = it.get("scene", f"Scene {it.get('index', 1)}")
            scene_idx = it.get("index", 1)
            is_video = it.get("type") == "AIV"

            print(f"  ✍️ [Account {acc_id}] Gửi prompt cho {scene_label} ({it['id']}): '{prompt_text[:50]}...'")

            # Bước 3: Inject prompt và Enter đúng 1 lần (không click button)
            session.inject_and_send_prompt(prompt_text)

            # Bước 4: Đợi tile hoàn tất và lấy kết quả
            ok, matched = session.wait_for_completion([scene_label], is_video=is_video)
            if ok and scene_label in matched and matched[scene_label].get("media_url"):
                media_url = matched[scene_label]["media_url"]
                sync_ok, path_or_err = sync_flow_media_to_studio(channel, slug, scene_idx, media_url, is_video=is_video)
                if sync_ok:
                    print(f"  ✅ [Account {acc_id}] Đã sync asset về Studio: {path_or_err}")
                    success_count += 1
                    # Schedule follow-up sync
                    schedule_followup_sync(session, channel, slug, scene_idx, scene_label, is_video)
                else:
                    print(f"  ⚠️ [Account {acc_id}] Lỗi sync media: {path_or_err}")
                    fail_count += 1
            else:
                print(f"  ⚠️ [Account {acc_id}] Hết timeout hoặc chưa có media URL cho {scene_label}")
                fail_count += 1
                # Vẫn kích hoạt follow-up sync đề phòng render trễ
                schedule_followup_sync(session, channel, slug, scene_idx, scene_label, is_video)

    except Exception as e:
        print(f"  ❌ [Account {acc_id}] Lỗi: {e}")
        fail_count += len(batch_items)
    finally:
        session.close()

    return success_count, fail_count


def run_dispatcher(channel=None, slug=None, dry_run=False):
    root_dir = ROOT_DIR
    channel, slug = resolve_active_video(root_dir, channel, slug)
    cfg = load_accounts_config()

    print("=" * 78)
    print("🚀 GOOGLE FLOW MULTI-ACCOUNT BATCH DISPATCHER")
    print(f"   Kênh: {channel} | Video: {slug}")
    print("=" * 78)

    # 1. Quét các account đang Online
    online_accounts = []
    for acc in cfg["accounts"]:
        is_online, _, _ = check_cdp_status(acc["port"])
        if is_online:
            online_accounts.append(acc)

    print(f"🔍 Kiểm tra tài khoản: {len(online_accounts)}/{len(cfg['accounts'])} accounts đang Online (CDP)")
    if not online_accounts and not dry_run:
        print("\n❌ Không có tài khoản Google Flow nào đang mở!")
        print("💡 Hãy chạy lệnh để mở các cửa sổ Chrome:")
        print("   • Mở 1 account để login : python tools/flow-dispatcher/browser_pool.py launch --acc 1")
        print("   • Mở toàn bộ 5 account  : python tools/flow-dispatcher/browser_pool.py launch-all")
        print("   • Đóng an toàn          : python tools/flow-dispatcher/browser_pool.py close-all")
        print("   • Hoặc thêm cờ '--dry-run' để kiểm tra kế hoạch phân bổ mà không cần mở Chrome.")
        sys.exit(1)

    accounts_to_use = online_accounts if online_accounts else cfg["accounts"]

    # 2. Đọc danh sách assets cần tạo
    items = load_video_prompts(root_dir, channel, slug)
    aiv_items = [it for it in items if it["type"] == "AIV"]
    img_items = [it for it in items if it["type"] != "AIV"]

    print(f"📋 Tổng số cảnh cần tạo: {len(items)} (🎬 AIV: {len(aiv_items)} | 🖼️ IMG: {len(img_items)})")
    print("-" * 78)

    # 3. Phân bổ thông minh (Quota-Aware Allocation)
    dest_dir = root_dir / "channels" / channel / "videos" / slug / "assets"
    dest_dir.mkdir(parents=True, exist_ok=True)

    allocations = {acc["id"]: [] for acc in accounts_to_use}

    # Phân bổ AIV (tốn credit) chia đều
    for idx, item in enumerate(aiv_items):
        target_acc = accounts_to_use[idx % len(accounts_to_use)]
        allocations[target_acc["id"]].append(item)

    # Phân bổ IMG (0 credit free) chia đều theo batch
    for idx, item in enumerate(img_items):
        target_acc = accounts_to_use[idx % len(accounts_to_use)]
        allocations[target_acc["id"]].append(item)

    print("📊 KẾ HOẠCH PHÂN BỔ THEO TÀI KHOẢN:")
    for acc in accounts_to_use:
        batch = allocations[acc["id"]]
        aiv_c = sum(1 for x in batch if x["type"] == "AIV")
        img_c = sum(1 for x in batch if x["type"] != "AIV")
        print(f"  • Account {acc['id']} ({acc['name']}, Port {acc['port']}): {len(batch)} tasks (🎬 {aiv_c} AIV, 🖼️ {img_c} IMG)")

    print("-" * 78)
    print("⚡ Bắt đầu thực thi song song qua ThreadPoolExecutor...")

    start_all = time.time()
    total_success = 0
    total_fail = 0

    with ThreadPoolExecutor(max_workers=len(accounts_to_use)) as executor:
        futures = []
        for acc in accounts_to_use:
            batch = allocations[acc["id"]]
            if batch:
                f = executor.submit(dispatch_worker, acc, batch, channel, slug, dry_run)
                futures.append(f)

        for f in futures:
            s, fl = f.result()
            total_success += s
            total_fail += fl

    elapsed = int(time.time() - start_all)
    print("=" * 78)
    print(f"🎉 HOÀN TẤT DISPATCH (Tổng thời gian: {elapsed}s)")
    print(f"   • Thành công: {total_success} / {len(items)}")
    print(f"   • Thất bại:   {total_fail}")
    print(f"   • Assets tại: {dest_dir}")
    print("=" * 78)


def main():
    parser = argparse.ArgumentParser(description="Google Flow Multi-Account Batch Dispatcher.")
    parser.add_argument("slug", nargs="?", default=None, help="Slug của video (ví dụ: thoat-bay-no-the-tin-dung)")
    parser.add_argument("--channel", default=None, help="Tên kênh (ví dụ: tien-thuc-chien)")
    parser.add_argument("--dry-run", action="store_true", help="Chạy mô phỏng không gửi lệnh qua Chrome CDP")

    args = parser.parse_args()
    run_dispatcher(channel=args.channel, slug=args.slug, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
