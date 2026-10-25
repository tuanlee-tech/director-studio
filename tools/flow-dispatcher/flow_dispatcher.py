#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
flow_dispatcher.py — Google Flow Multi-Account Batch Dispatcher
Điều phối tự động phân chia prompt video cho 5 tài khoản Google Flow qua CDP.
Tận dụng tối đa quota credit hàng ngày (250 credit video / 5 account) và cào ảnh 0 credit song song.
"""

import sys
import os
import json
import time
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

try:
    from chrome_launcher import load_accounts_config, check_cdp_status, get_active_tabs
    from cdp_client import FlowCDPClient
except ImportError:
    from tools.flow_dispatcher.chrome_launcher import load_accounts_config, check_cdp_status, get_active_tabs
    from tools.flow_dispatcher.cdp_client import FlowCDPClient

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
    """Đọc danh sách B-roll và prompts từ broll-plan.json hoặc prompts.md."""
    video_dir = root_dir / "channels" / channel / "videos" / slug
    broll_file = video_dir / "broll-plan.json"
    prompts_file = video_dir / "assets" / "prompts.md"

    items = []
    if broll_file.exists():
        try:
            data = json.loads(broll_file.read_text(encoding="utf-8"))
            for b in data:
                items.append({
                    "id": b.get("broll_id", "S001-A"),
                    "scene": b.get("scene", "S001"),
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
        {"id": "S001-A", "scene": "S001", "type": "AIV", "duration": 6, "target_file": "S001-A_6s_AIV.mp4", "prompt": "Man looking shocked at red credit card bill, 2D vector style"},
        {"id": "S002-A", "scene": "S002", "type": "AIV", "duration": 4, "target_file": "S002-A_4s_AIV.mp4", "prompt": "Salary notification arrives on phone, 2D vector style"},
        {"id": "S003-A", "scene": "S003", "type": "IMG", "duration": 4, "target_file": "S003-A_IMG.png", "prompt": "Credit card cut in half with scissors on table, 2D vector style"},
        {"id": "S004-A", "scene": "S004", "type": "IMG", "duration": 4, "target_file": "S004-A_IMG.png", "prompt": "Financial freedom roadmap with green upward chart, 2D vector style"}
    ]

def dispatch_worker(acc_info, batch_items, dest_dir, dry_run=False):
    """Worker xử lý batch prompts cho 1 tài khoản Chrome."""
    acc_id = acc_info["id"]
    port = acc_info["port"]
    name = acc_info["name"]

    print(f"\n[Account {acc_id} - {name}] Bắt đầu xử lý {len(batch_items)} items...")

    if dry_run:
        for it in batch_items:
            print(f"  👉 [Account {acc_id}] Mock dispatch: {it['id']} ({it['type']}) → {it['target_file']}")
            time.sleep(0.5)
        return len(batch_items), 0

    client = FlowCDPClient(port=port)
    success_count = 0
    fail_count = 0

    try:
        client.connect()
        page_info = client.check_page_loaded()
        print(f"  🔗 [Account {acc_id}] Đã kết nối tab: {page_info.get('title', 'Flow')}")

        for it in batch_items:
            prompt_text = it["prompt"]
            print(f"  ✍️ [Account {acc_id}] Gửi prompt {it['id']}: '{prompt_text[:40]}...'")
            
            res = client.inject_and_send_prompt(prompt_text)
            if res and res.get("success"):
                print(f"  ⏳ [Account {acc_id}] Đang chờ Google Flow phản hồi cho {it['id']}...")
                # Chờ response (thực tế khoảng 15-40s)
                time.sleep(6)
                success_count += 1
            else:
                print(f"  ⚠️ [Account {acc_id}] Không thể gửi prompt cho {it['id']}")
                fail_count += 1
    except Exception as e:
        print(f"  ❌ [Account {acc_id}] Lỗi: {e}")
        fail_count += len(batch_items)
    finally:
        client.close()

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
        is_online, _ = check_cdp_status(acc["port"])
        if is_online:
            online_accounts.append(acc)

    print(f"🔍 Kiểm tra tài khoản: {len(online_accounts)}/{len(cfg['accounts'])} accounts đang Online (CDP)")
    if not online_accounts and not dry_run:
        print("\n❌ Không có tài khoản Google Flow nào đang mở!")
        print("💡 Hãy chạy lệnh để mở các cửa sổ Chrome:")
        print("   • Mở 1 account để login : python tools/flow-dispatcher/chrome_launcher.py login --acc 1")
        print("   • Mở toàn bộ 5 account  : python tools/flow-dispatcher/chrome_launcher.py start-all")
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

    # In kế hoạch phân bổ
    print("📊 KẾ HOẠCH PHÂN BỔ CÔNG VIỆC CHO CÁC TÀI KHOẢN:")
    for acc in accounts_to_use:
        acc_id = acc["id"]
        tasks = allocations[acc_id]
        aiv_c = sum(1 for t in tasks if t["type"] == "AIV")
        img_c = sum(1 for t in tasks if t["type"] != "AIV")
        est_credits = aiv_c * 20 # Ước lượng ~20 credit/clip video
        print(f"  • Account {acc_id} ({acc['name']:<16}) : {len(tasks):<2} items (AIV: {aiv_c}, IMG: {img_c}) → Ước tính credit: {est_credits}/50")

    print("-" * 78)

    # 4. Thực thi song song (Multithreading)
    print("⚡ Bắt đầu dispatch song song tới các cửa sổ Chrome...")
    total_success = 0
    total_fail = 0

    with ThreadPoolExecutor(max_workers=len(accounts_to_use)) as executor:
        futures = []
        for acc in accounts_to_use:
            acc_id = acc["id"]
            batch = allocations[acc_id]
            if batch:
                futures.append(executor.submit(dispatch_worker, acc, batch, dest_dir, dry_run=dry_run))

        for f in futures:
            s, fl = f.result()
            total_success += s
            total_fail += fl

    print("\n" + "=" * 78)
    print(f"🎉 HOÀN TẤT ĐIỀU PHỐI GOOGLE FLOW MULTI-ACCOUNT!")
    print(f"   • Thành công : {total_success} items")
    print(f"   • Thất bại   : {total_fail} items")
    print(f"   • Thư mục lưu: {dest_dir}")
    print("=" * 78)

def main():
    parser = argparse.ArgumentParser(description="Google Flow Multi-Account Batch Dispatcher.")
    parser.add_argument("slug", nargs="?", default=None, help="Slug của video (ví dụ: thoat-bay-no-the-tin-dung)")
    parser.add_argument("--channel", default=None, help="Tên kênh (mặc định lấy active channel)")
    parser.add_argument("--dry-run", action="store_true", help="Chạy thử nghiệm mô phỏng phân bổ không cần kết nối Chrome")

    args = parser.parse_args()
    run_dispatcher(channel=args.channel, slug=args.slug, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
