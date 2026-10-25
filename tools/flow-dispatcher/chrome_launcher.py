#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chrome_launcher.py — Google Flow Multi-Account Chrome Launcher
Quản lý các phiên Chrome độc lập với Chrome Remote Debugging Protocol (CDP).
Mỗi tài khoản có thư mục User Data riêng biệt, lưu giữ session/cookie vĩnh viễn.
"""

import sys
import os
import json
import time
import shutil
import subprocess
import argparse
from pathlib import Path
import urllib.request
import urllib.error

# Fix UTF-8 console output for Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent.parent
CONFIG_FILE = SCRIPT_DIR / "accounts.json"
PROFILES_DIR = SCRIPT_DIR / "profiles"

def find_chrome_executable():
    """Tự động tìm kiếm đường dẫn Chrome trên các hệ điều hành."""
    if sys.platform == "win32":
        candidates = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%PROGRAMFILES%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%PROGRAMFILES(X86)%\Google\Chrome\Application\chrome.exe"),
        ]
        for path in candidates:
            if os.path.isfile(path):
                return path
        # Thử tìm qua PATH
        which_chrome = shutil.which("chrome.exe") or shutil.which("chrome")
        if which_chrome:
            return which_chrome
    elif sys.platform == "darwin":
        mac_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        if os.path.isfile(mac_path):
            return mac_path
    else: # Linux
        for bin_name in ["google-chrome", "google-chrome-stable", "chromium-browser", "chromium"]:
            which_bin = shutil.which(bin_name)
            if which_bin:
                return which_bin

    return None

def load_accounts_config():
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(f"Không tìm thấy file cấu hình {CONFIG_FILE}")
    return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))

def save_accounts_config(data):
    CONFIG_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

def check_cdp_status(port):
    """Kiểm tra xem port CDP có đang phản hồi không."""
    url = f"http://127.0.0.1:{port}/json/version"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=1.5) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode("utf-8"))
                return True, data.get("Browser", "Chrome CDP Online")
    except Exception:
        pass
    return False, "Offline"

def get_active_tabs(port):
    """Lấy danh sách các tab đang mở tại port CDP."""
    url = f"http://127.0.0.1:{port}/json/list"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=1.5) as resp:
            if resp.status == 200:
                return json.loads(resp.read().decode("utf-8"))
    except Exception:
        pass
    return []

def launch_account(acc_id, target_url=None):
    """Khởi động 1 cửa sổ Chrome với Profile riêng và Debug Port tương ứng."""
    chrome_path = find_chrome_executable()
    if not chrome_path:
        print("❌ Không tìm thấy Google Chrome trên máy tính của bạn.")
        print("Vui lòng tải và cài đặt Google Chrome: https://www.google.com/chrome/")
        return 1

    cfg = load_accounts_config()
    acc = next((a for a in cfg["accounts"] if a["id"] == int(acc_id)), None)
    if not acc:
        print(f"❌ Không tìm thấy cấu hình cho Account ID: {acc_id}")
        return 1

    port = acc["port"]
    profile_path = SCRIPT_DIR / acc["profile_dir"]
    profile_path.mkdir(parents=True, exist_ok=True)

    url = target_url or cfg.get("default_flow_url", "https://flow.google.com")

    # Kiểm tra xem port này đã chạy chưa
    is_online, browser_name = check_cdp_status(port)
    if is_online:
        print(f"⚡ Account {acc_id} ({acc['name']}) đã ĐANG CHẠY tại port {port} ({browser_name})!")
        return 0

    cmd = [
        chrome_path,
        f"--remote-debugging-port={port}",
        f"--user-data-dir={profile_path}",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-background-networking",
        url
    ]

    print("=" * 72)
    print(f"🚀 KHỞI ĐỘNG CHROME CHO TÀI KHOẢN {acc_id} ({acc['name']})")
    print(f"   • Debugging Port : {port}")
    print(f"   • User Profile   : {profile_path}")
    print(f"   • Target URL     : {url}")
    print("=" * 72)
    print("👉 Hãy đăng nhập Google và vào Flow project trên cửa sổ vừa mở.")
    print("   (Session và Cookie sẽ tự động lưu vĩnh viễn trong profile này)")

    # Khởi chạy không chặn console
    if sys.platform == "win32":
        subprocess.Popen(cmd, creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
    else:
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)

    # Đợi 2-3s để Chrome bind port
    for _ in range(6):
        time.sleep(1)
        ok, _ = check_cdp_status(port)
        if ok:
            print(f"✅ Đã kết nối thành công tới Chrome CDP trên port {port}!")
            return 0

    print(f"⚠️ Đã gửi lệnh mở Chrome. Vui lòng kiểm tra trên màn hình.")
    return 0

def action_status():
    """In bảng trạng thái 5 tài khoản."""
    cfg = load_accounts_config()
    print("=" * 78)
    print("🌐 GOOGLE FLOW MULTI-ACCOUNT DISPATCHER STATUS")
    print("=" * 78)
    print(f"{'ID':<4} {'Tên Account':<18} {'Port':<8} {'Trạng thái':<14} {'Active Tab / Project':<30}")
    print("-" * 78)

    for acc in cfg["accounts"]:
        port = acc["port"]
        is_online, info = check_cdp_status(port)
        status_text = "🟢 Online" if is_online else "⚪ Offline"
        
        tab_info = "Chưa kết nối"
        if is_online:
            tabs = get_active_tabs(port)
            flow_tab = next((t for t in tabs if "flow.google.com" in t.get("url", "")), None)
            if flow_tab:
                tab_info = flow_tab.get("title", "Google Flow Tab")[:28]
            elif tabs:
                tab_info = tabs[0].get("title", "Unknown Tab")[:28]
            else:
                tab_info = "Chrome đang mở"

        print(f"{acc['id']:<4} {acc['name']:<18} {port:<8} {status_text:<14} {tab_info:<30}")

    print("=" * 78)
    print("💡 Hướng dẫn:")
    print("   • Đăng nhập tài khoản : python chrome_launcher.py login --acc <1..5>")
    print("   • Mở tất cả cửa sổ    : python chrome_launcher.py start-all")
    print("=" * 78)

def action_start_all():
    """Khởi động toàn bộ 5 tài khoản."""
    cfg = load_accounts_config()
    print("🚀 Bắt đầu khởi động toàn bộ các tài khoản Chrome...")
    for acc in cfg["accounts"]:
        launch_account(acc["id"])
        time.sleep(1.5)
    action_status()

def main():
    parser = argparse.ArgumentParser(description="Google Flow Multi-Account Chrome Launcher.")
    parser.add_argument("command", nargs="?", default="status", choices=["login", "status", "start-all", "start"],
                        help="Lệnh: login (mở 1 acc), status (xem trạng thái), start-all (mở toàn bộ)")
    parser.add_argument("--acc", type=int, default=1, help="ID của tài khoản (1 đến 5)")
    parser.add_argument("--url", default=None, help="URL tùy chọn mở khi khởi động")

    args = parser.parse_args()

    if args.command in ["login", "start"]:
        sys.exit(launch_account(args.acc, target_url=args.url))
    elif args.command == "start-all":
        action_start_all()
    else:
        action_status()

if __name__ == "__main__":
    main()
