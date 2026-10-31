#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
launch_chrome_daemon.py
Khởi chạy và duy trì 5 Chrome instances cho 5 tài khoản Google Flow (ports 9223-9227).
Chạy dưới dạng Daemon để giữ process sống trong suốt phiên làm việc.
"""

import os
import sys
import time
import subprocess
from pathlib import Path

# Fix UTF-8 console output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
HOME = os.path.expanduser("~")

ACCOUNTS = [
    {
        "id": 1,
        "port": 9223,
        "profile": os.path.join(HOME, ".flowkit", "chrome_acc1"),
        "url": "https://flow.google.com/project/aee9b642-b464-49c4-86dd-026118888bc9"
    },
    {
        "id": 2,
        "port": 9224,
        "profile": os.path.join(HOME, ".flowkit", "chrome_acc2"),
        "url": "https://flow.google.com/project/7380fc82-217e-4cab-ad87-0276ade42bc7"
    },
    {
        "id": 3,
        "port": 9225,
        "profile": os.path.join(HOME, ".flowkit", "chrome_acc3"),
        "url": "https://flow.google.com/project/60492441-1bc3-4a1c-bdc6-b1e29c748b4b"
    },
    {
        "id": 4,
        "port": 9226,
        "profile": os.path.join(HOME, ".flowkit", "chrome_acc4"),
        "url": "https://flow.google.com/project/e9a9156f-0a9b-46f1-b8b8-7a3a535bcf98"
    },
    {
        "id": 5,
        "port": 9227,
        "profile": os.path.join(HOME, ".flowkit", "chrome_acc5"),
        "url": "https://flow.google.com/project/9c3b38df-6e67-464c-af83-fa76fd8fcd59"
    }
]

processes = []

print("🚀 Khởi chạy 5 Chrome Instances cho Google Flow...")
for acc in ACCOUNTS:
    cmd = [
        CHROME_PATH,
        f"--remote-debugging-port={acc['port']}",
        f"--user-data-dir={acc['profile']}",
        "--remote-allow-origins=*",
        "--no-first-run",
        "--no-default-browser-check",
        acc["url"]
    ]
    p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    processes.append((acc["id"], acc["port"], p))
    print(f"  • Acc {acc['id']} (Port {acc['port']}) -> PID {p.pid}")
    time.sleep(1)

print("\n✅ Đã khởi chạy xong toàn bộ 5 Chrome instances. Đang duy trì Daemon...")
try:
    while True:
        time.sleep(10)
        # Check if any process died
        for acc_id, port, p in processes:
            if p.poll() is not None:
                print(f"⚠️ Acc {acc_id} (Port {port}) đã thoát với code {p.returncode}")
except KeyboardInterrupt:
    print("\n🛑 Nhận tín hiệu dừng, đóng các process...")
    for _, _, p in processes:
        p.terminate()
