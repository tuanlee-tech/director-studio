#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
browser_pool.py — Google Flow Multi-Account Chrome Browser Pool
Quản lý vòng đời tiến trình Chrome (Spawn, Status, Safe Close via CDP Browser.close).
Hỗ trợ đa tài khoản độc lập, lưu giữ cookie/session vĩnh viễn, chống popup Restore pages.
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

try:
    import websocket
except ImportError:
    websocket = None


def find_chrome_executable():
    """Tự động tìm kiếm đường dẫn Chrome trên Windows, macOS, Linux."""
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
        which_chrome = shutil.which("chrome.exe") or shutil.which("chrome")
        if which_chrome:
            return which_chrome
    elif sys.platform == "darwin":
        mac_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        if os.path.isfile(mac_path):
            return mac_path
    else:  # Linux
        for bin_name in ["google-chrome", "google-chrome-stable", "chromium-browser", "chromium"]:
            which_bin = shutil.which(bin_name)
            if which_bin:
                return which_bin

    return None


def resolve_profile_path(profile_dir_str):
    """Mở rộng đường dẫn profile (hỗ trợ ~ và relative path)."""
    if profile_dir_str.startswith("~"):
        p = Path(os.path.expanduser(profile_dir_str)).resolve()
    else:
        p = (SCRIPT_DIR / profile_dir_str).resolve()
    p.mkdir(parents=True, exist_ok=True)
    return str(p)


def load_accounts_config():
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(f"Không tìm thấy file cấu hình {CONFIG_FILE}")
    return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))


def save_accounts_config(data):
    CONFIG_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def check_cdp_status(port):
    """Kiểm tra xem port CDP có đang phản hồi không (nhanh chóng với socket check trước)."""
    # Quick socket probe (tránh chờ timeout HTTP lâu khi port đóng)
    import socket
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=0.15):
            pass
    except Exception:
        return False, "Offline", None

    url = f"http://127.0.0.1:{port}/json/version"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=1.5) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode("utf-8"))
                return True, data.get("Browser", "Chrome CDP Online"), data.get("webSocketDebuggerUrl")
    except Exception:
        pass
    return False, "Offline", None


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


def _win32_spawn_interactive(cmd_list):
    """
    Sử dụng trực tiếp Win32 CreateProcessW với lpDesktop='Default'
    để ép buộc cửa sổ GUI hiển thị trên màn hình tương tác thực tế của người dùng,
    bất kể tiến trình gọi đang chạy ở background hay sandbox desktop nào.
    """
    import ctypes
    from ctypes import wintypes

    class STARTUPINFOW(ctypes.Structure):
        _fields_ = [
            ("cb", wintypes.DWORD),
            ("lpReserved", wintypes.LPWSTR),
            ("lpDesktop", wintypes.LPWSTR),
            ("lpTitle", wintypes.LPWSTR),
            ("dwX", wintypes.DWORD),
            ("dwY", wintypes.DWORD),
            ("dwXSize", wintypes.DWORD),
            ("dwYSize", wintypes.DWORD),
            ("dwXCountChars", wintypes.DWORD),
            ("dwYCountChars", wintypes.DWORD),
            ("dwFillAttribute", wintypes.DWORD),
            ("dwFlags", wintypes.DWORD),
            ("wShowWindow", wintypes.WORD),
            ("cbReserved2", wintypes.WORD),
            ("lpReserved2", ctypes.c_char_p),
            ("hStdInput", wintypes.HANDLE),
            ("hStdOutput", wintypes.HANDLE),
            ("hStdError", wintypes.HANDLE),
        ]

    class PROCESS_INFORMATION(ctypes.Structure):
        _fields_ = [
            ("hProcess", wintypes.HANDLE),
            ("hThread", wintypes.HANDLE),
            ("dwProcessId", wintypes.DWORD),
            ("dwThreadId", wintypes.DWORD),
        ]

    kernel32 = ctypes.windll.kernel32

    # Ghép chuỗi command line chuẩn Windows
    parts = []
    for arg in cmd_list:
        if " " in arg and not arg.startswith('"'):
            parts.append(f'"{arg}"')
        else:
            parts.append(arg)
    cmd_line = " ".join(parts)

    si = STARTUPINFOW()
    si.cb = ctypes.sizeof(STARTUPINFOW)
    si.lpDesktop = "Default"
    si.dwFlags = 1  # STARTF_USESHOWWINDOW
    si.wShowWindow = 1  # SW_SHOWNORMAL

    pi = PROCESS_INFORMATION()

    # Thử CREATE_BREAKAWAY_FROM_JOB (0x01000000) | DETACHED_PROCESS (0x00000008)
    creation_flags = 0x01000000 | 0x00000008
    success = kernel32.CreateProcessW(
        None,
        cmd_line,
        None,
        None,
        False,
        creation_flags,
        None,
        None,
        ctypes.byref(si),
        ctypes.byref(pi),
    )

    if not success:
        # Fallback sang CREATE_NEW_PROCESS_GROUP
        creation_flags = 0x00000200
        success = kernel32.CreateProcessW(
            None,
            cmd_line,
            None,
            None,
            False,
            creation_flags,
            None,
            None,
            ctypes.byref(si),
            ctypes.byref(pi),
        )

    if success:
        kernel32.CloseHandle(pi.hProcess)
        kernel32.CloseHandle(pi.hThread)
        return True, pi.dwProcessId
    else:
        err = kernel32.GetLastError()
        return False, f"Win32 Error: {err}"


def launch_account(account_id, project_url=None):
    """Khởi động 1 cửa sổ Chrome với Profile riêng và Debug Port tương ứng."""
    chrome_path = find_chrome_executable()
    if not chrome_path:
        print("❌ Không tìm thấy Google Chrome trên máy tính.")
        return False, "Chrome not found"

    cfg = load_accounts_config()
    acc = next((a for a in cfg["accounts"] if a["id"] == int(account_id)), None)
    if not acc:
        return False, f"Account ID {account_id} not found"

    port = acc["port"]
    profile_path = resolve_profile_path(acc.get("profile_dir", f"profiles/acc{account_id}"))

    # Xác định URL mở: project_url chỉ định > acc project_url > default project url > flow.google.com
    target_url = (
        project_url
        or acc.get("project_url")
        or cfg.get("default_project_url")
        or cfg.get("default_flow_url", "https://flow.google.com")
    )
    if not target_url.strip():
        target_url = "https://flow.google.com"

    # Kiểm tra xem port này đã chạy chưa
    is_online, browser_name, _ = check_cdp_status(port)
    if is_online:
        print(f"⚡ Account {account_id} ({acc['name']}) đã ĐANG CHẠY tại port {port} ({browser_name})!")
        return True, f"Already running on port {port}"

    cmd = [
        chrome_path,
        f"--remote-debugging-port={port}",
        f"--user-data-dir={profile_path}",
        "--remote-allow-origins=*",
        "--no-first-run",
        "--no-default-browser-check",
        target_url,
    ]

    print("=" * 72)
    print(f"🚀 KHỞI ĐỘNG CHROME CHO TÀI KHOẢN {account_id} ({acc['name']})")
    print(f"   • Debugging Port : {port}")
    print(f"   • User Profile   : {profile_path}")
    print(f"   • Target URL     : {target_url}")
    print("=" * 72)

    # Spawn Chrome với Win32 Desktop tương tác (Default) trên Windows
    if sys.platform == "win32":
        ok, res = _win32_spawn_interactive(cmd)
        if not ok:
            print(f"⚠️ Win32 spawn failed ({res}), falling back to subprocess.Popen")
            subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    else:
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)

    # Đợi Chrome bind port
    for _ in range(8):
        time.sleep(1)
        ok, _, _ = check_cdp_status(port)
        if ok:
            print(f"✅ Đã kết nối thành công tới Chrome CDP trên port {port}!")
            return True, f"Online on port {port}"

    return True, "Chrome process launched (waiting for window)"


def close_account(account_id):
    """
    Đóng Chrome an toàn qua CDP command: Browser.close.
    Không kill port cứng → Chrome tự lưu cookie, flush profile và không bao giờ hiện prompt 'Restore pages?'.
    """
    cfg = load_accounts_config()
    acc = next((a for a in cfg["accounts"] if a["id"] == int(account_id)), None)
    if not acc:
        return False, f"Account ID {account_id} not found"

    port = acc["port"]
    is_online, _, ws_browser_url = check_cdp_status(port)
    if not is_online:
        return True, "Already offline"

    if not websocket:
        return False, "websocket-client package is required for graceful close"

    # Gửi lệnh Browser.close qua browser WebSocket
    if ws_browser_url:
        try:
            ws = websocket.create_connection(ws_browser_url, timeout=5)
            ws.send(json.dumps({"id": 9999, "method": "Browser.close"}))
            ws.close()
            time.sleep(1)
            return True, f"Account {account_id} closed gracefully"
        except Exception as e:
            print(f"⚠️ Không thể gửi Browser.close qua ws_browser_url: {e}")

    # Fallback: Thử qua tab đầu tiên
    tabs = get_active_tabs(port)
    for t in tabs:
        tab_ws = t.get("webSocketDebuggerUrl")
        if tab_ws:
            try:
                ws = websocket.create_connection(tab_ws, timeout=5)
                ws.send(json.dumps({"id": 9999, "method": "Browser.close"}))
                ws.close()
                time.sleep(1)
                return True, f"Account {account_id} closed gracefully via tab"
            except Exception:
                pass

    return False, "Failed to send Browser.close command"


def launch_all(project_url=None):
    """Mở tất cả 5 tài khoản Chrome."""
    cfg = load_accounts_config()
    results = {}
    for acc in cfg["accounts"]:
        ok, msg = launch_account(acc["id"], project_url=project_url)
        results[acc["id"]] = {"success": ok, "message": msg}
        time.sleep(1.5)
    return results


def close_all():
    """Đóng tất cả 5 tài khoản Chrome một cách an toàn."""
    cfg = load_accounts_config()
    results = {}
    for acc in cfg["accounts"]:
        ok, msg = close_account(acc["id"])
        results[acc["id"]] = {"success": ok, "message": msg}
        time.sleep(0.5)
    return results


def get_accounts():
    """Lấy danh sách các tài khoản kèm trạng thái CDP realtime."""
    cfg = load_accounts_config()
    result = []

    for acc in cfg.get("accounts", []):
        port = acc["port"]
        is_online, browser_name, _ = check_cdp_status(port)
        tabs = get_active_tabs(port) if is_online else []

        flow_tab = next((t for t in tabs if "flow.google.com" in t.get("url", "")), None)
        active_tab_title = flow_tab.get("title", "Google Flow") if flow_tab else (tabs[0].get("title", "Chrome") if tabs else "None")
        tab_url = flow_tab.get("url") if flow_tab else (tabs[0].get("url") if tabs else "")
        flow_tab_open = flow_tab is not None

        result.append({
            "account_id": acc["id"],
            "id": acc["id"],
            "name": acc["name"],
            "port": port,
            "profile_dir": acc.get("profile_dir"),
            "project_url": acc.get("project_url", ""),
            "cdp_available": is_online,
            "browser_name": browser_name,
            "flow_tab_open": flow_tab_open,
            "tab_url": tab_url,
            "active_tab_title": active_tab_title,
            "daily_credit_limit": acc.get("daily_credit_limit", 50),
            "credit_used_today": acc.get("credit_used_today", 0),
        })

    return result


def main():
    parser = argparse.ArgumentParser(description="Google Flow Multi-Account Chrome Browser Pool.")
    parser.add_argument("command", nargs="?", default="status", choices=["launch", "close", "status", "launch-all", "close-all"])
    parser.add_argument("--acc", type=int, default=1, help="ID của tài khoản (1-5)")
    parser.add_argument("--url", default=None, help="Project URL hoặc Target URL")

    args = parser.parse_args()

    if args.command == "launch":
        ok, msg = launch_account(args.acc, project_url=args.url)
        print(f"[{'OK' if ok else 'ERR'}] {msg}")
    elif args.command == "close":
        ok, msg = close_account(args.acc)
        print(f"[{'OK' if ok else 'ERR'}] {msg}")
    elif args.command == "launch-all":
        launch_all(project_url=args.url)
    elif args.command == "close-all":
        close_all()
    else:
        accounts = get_accounts()
        print("=" * 86)
        print("🌐 GOOGLE FLOW MULTI-ACCOUNT BROWSER POOL STATUS")
        print("=" * 86)
        print(f"{'ID':<4} {'Tên':<16} {'Port':<8} {'CDP':<10} {'Flow Tab':<12} {'Tab URL / Title':<32}")
        print("-" * 86)
        for a in accounts:
            cdp_str = "🟢 Online" if a["cdp_available"] else "⚪ Offline"
            flow_str = "✅ Đang mở" if a["flow_tab_open"] else "❌ Chưa mở"
            info_str = (a["active_tab_title"] or a["tab_url"] or "")[:30]
            print(f"{a['id']:<4} {a['name']:<16} {a['port']:<8} {cdp_str:<10} {flow_str:<12} {info_str:<32}")
        print("=" * 86)


if __name__ == "__main__":
    main()
