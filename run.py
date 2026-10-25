#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run.py — Unified Cross-Platform Project Starter (Ubuntu / Windows / macOS)
Khởi động toàn bộ dự án AI Audio & Video Platform chỉ với 1 lệnh duy nhất:
    python run.py (hoặc python3 run.py)

Tự động điều phối:
1. VieNeu-TTS Engine (Port 7860)
2. Studio Management Dashboard & Remotion Engine (Port 3000)
3. Google Flow Multi-Account CDP Dispatcher (Ports 9223-9227)
"""

import sys
import os
import time
import signal
import shutil
import socket
import subprocess
import argparse
import urllib.request
from pathlib import Path

# Fix UTF-8 console output for Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent
TTS_DIR = ROOT_DIR / "VieNeu-TTS"
STUDIO_DIR = ROOT_DIR / "studio"
REMOTION_DIR = STUDIO_DIR / "remotion"
PIDFILE_TTS = ROOT_DIR / ".tts.pid"
PIDFILE_STUDIO = ROOT_DIR / ".studio.pid"

IS_WIN = sys.platform == "win32"
IS_LINUX = sys.platform.startswith("linux")
IS_MAC = sys.platform == "darwin"


def print_banner():
    print("""
\033[1;36m========================================================================\033[0m
\033[1;32m  🎬 AI AUDIO & VIDEO STUDIO — UNIFIED PLATFORM STARTER\033[0m
\033[1;36m========================================================================\033[0m
  • OS:         \033[1m""" + sys.platform + """\033[0m
  • Python:     \033[1m""" + sys.version.split()[0] + """\033[0m
  • Root Dir:   """ + str(ROOT_DIR) + """
\033[1;36m========================================================================\033[0m
""")


def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.3)
        return s.connect_ex(("127.0.0.1", port)) == 0


def get_studio_python():
    """Lấy đường dẫn python venv của Studio."""
    if IS_WIN:
        py_bin = STUDIO_DIR / "venv" / "Scripts" / "python.exe"
    else:
        py_bin = STUDIO_DIR / "venv" / "bin" / "python"
    return py_bin


def get_tts_python():
    """Lấy đường dẫn python venv của VieNeu-TTS."""
    if IS_WIN:
        py_bin = TTS_DIR / ".venv" / "Scripts" / "python.exe"
    else:
        py_bin = TTS_DIR / ".venv" / "bin" / "python"
    if py_bin.exists():
        return py_bin
    return None


def ensure_studio_environment():
    """Kiểm tra và tự động cài đặt venv + dependencies cho Studio."""
    studio_py = get_studio_python()
    if not studio_py.exists():
        print("📦 Tạo virtual environment cho Studio tại studio/venv...")
        subprocess.run([sys.executable, "-m", "venv", str(STUDIO_DIR / "venv")], check=True)

    # Cài đặt requirements
    req_file = STUDIO_DIR / "requirements.txt"
    if req_file.exists():
        pip_bin = studio_py.parent / ("pip.exe" if IS_WIN else "pip")
        try:
            # Kiểm tra xem websocket-client đã cài chưa
            check_code = subprocess.run([str(studio_py), "-c", "import flask, requests, websocket"], capture_output=True)
            if check_code.returncode != 0:
                print("📦 Đang cài đặt thư viện phụ thuộc cho Studio (Flask, Requests, WebSocket)...")
                subprocess.run([str(pip_bin), "install", "-q", "-r", str(req_file)], check=True)
        except Exception as e:
            print(f"⚠️ Kiểm tra dependencies Studio: {e}")

    # Kiểm tra Remotion npm
    if REMOTION_DIR.exists() and not (REMOTION_DIR / "node_modules").exists():
        npm_bin = shutil.which("npm.cmd" if IS_WIN else "npm")
        if npm_bin:
            print("📦 Cài đặt thư viện Remotion (npm install)...")
            try:
                subprocess.run([npm_bin, "install", "--silent"], cwd=str(REMOTION_DIR), check=True)
                print("✅ Remotion dependencies đã sẵn sàng!")
            except Exception as e:
                print(f"⚠️ Cài đặt Remotion npm thất bại: {e}")


def start_tts_service():
    """Khởi chạy VieNeu-TTS trên cổng 7860."""
    if is_port_in_use(7860):
        print("✅ VieNeu-TTS đã ĐANG CHẠY tại http://localhost:7860")
        return None

    tts_py = get_tts_python()
    if not tts_py:
        print("⚠️ Không tìm thấy VieNeu-TTS venv tại VieNeu-TTS/.venv. Bỏ qua bước khởi động TTS.")
        return None

    print("🚀 Đang khởi động VieNeu-TTS engine trên cổng 7860...")
    log_out = open(TTS_DIR / "vieneu-web.stdout.log", "a", encoding="utf-8")
    log_err = open(TTS_DIR / "vieneu-web.stderr.log", "a", encoding="utf-8")

    creationflags = 0
    if IS_WIN:
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP

    proc = subprocess.Popen(
        [str(tts_py), "apps/gradio_main.py"],
        cwd=str(TTS_DIR),
        stdout=log_out,
        stderr=log_err,
        creationflags=creationflags
    )

    PIDFILE_TTS.write_text(str(proc.pid))
    return proc


def start_studio_service():
    """Khởi chạy Studio Web UI trên cổng 3000."""
    if is_port_in_use(3000):
        print("✅ Studio UI đã ĐANG CHẠY tại http://localhost:3000")
        return None

    studio_py = get_studio_python()
    print("🚀 Đang khởi động AI Audio & Video Studio UI trên cổng 3000...")

    env = os.environ.copy()
    env["PORT"] = "3000"
    env["VIENEU_TTS_URL"] = "http://localhost:7860"

    creationflags = 0
    if IS_WIN:
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP

    proc = subprocess.Popen(
        [str(studio_py), "app.py"],
        cwd=str(STUDIO_DIR),
        env=env,
        creationflags=creationflags
    )

    PIDFILE_STUDIO.write_text(str(proc.pid))
    return proc


def stop_all_services():
    """Dừng toàn bộ các tiến trình TTS và Studio."""
    print("🛑 Đang dừng toàn bộ các dịch vụ dự án...")

    for pid_file, name in [(PIDFILE_TTS, "VieNeu-TTS"), (PIDFILE_STUDIO, "Studio")]:
        if pid_file.exists():
            try:
                pid = int(pid_file.read_text().strip())
                if IS_WIN:
                    subprocess.run(["taskkill", "/F", "/T", "/PID", str(pid)], capture_output=True)
                else:
                    os.kill(pid, signal.SIGTERM)
                print(f"  • Đã dừng {name} (PID: {pid})")
            except Exception:
                pass
            try:
                pid_file.unlink()
            except Exception:
                pass

    # Giải phóng các cổng 3000 và 7860
    if IS_WIN:
        for port in [3000, 7860]:
            try:
                res = subprocess.run(f'netstat -ano | findstr :{port}', shell=True, capture_output=True, text=True)
                for line in res.stdout.splitlines():
                    parts = line.strip().split()
                    if len(parts) >= 5 and f":{port}" in parts[1] and parts[3] == "LISTENING":
                        p = parts[4]
                        subprocess.run(["taskkill", "/F", "/PID", p], capture_output=True)
            except Exception:
                pass
    else:
        for port in [3000, 7860]:
            try:
                subprocess.run(f"fuser -k {port}/tcp", shell=True, capture_output=True)
            except Exception:
                pass

    print("✅ Toàn bộ dịch vụ đã dừng thành công!")


def show_status():
    """Kiểm tra trạng thái realtime của toàn bộ nền tảng."""
    print("\n🌐 BẢNG TRẠNG THÁI HỆ THỐNG:")
    print("-" * 65)

    tts_ok = is_port_in_use(7860)
    studio_ok = is_port_in_use(3000)

    print(f"  • VieNeu-TTS (Port 7860) : {'🟢 ONLINE  (http://localhost:7860)' if tts_ok else '⚪ OFFLINE'}")
    print(f"  • Studio UI  (Port 3000) : {'🟢 ONLINE  (http://localhost:3000)' if studio_ok else '⚪ OFFLINE'}")

    # Kiểm tra 5 cổng Google Flow CDP
    print("\n  • Google Flow CDP Ports (9223 - 9227):")
    for p in range(9223, 9228):
        c_ok = is_port_in_use(p)
        print(f"      Port {p} (Account {p - 9222}): {'🟢 Online' if c_ok else '⚪ Offline'}")
    print("-" * 65)


def main():
    parser = argparse.ArgumentParser(description="AI Audio & Video Platform Unified Starter.")
    parser.add_argument("--stop", action="store_true", help="Dừng tất cả các dịch vụ đang chạy")
    parser.add_argument("--status", action="store_true", help="Xem trạng thái các dịch vụ")
    parser.add_argument("--studio-only", action="store_true", help="Chỉ khởi chạy Studio Web UI (Port 3000)")
    parser.add_argument("--tts-only", action="store_true", help="Chỉ khởi chạy VieNeu-TTS (Port 7860)")

    args = parser.parse_args()

    if args.stop:
        stop_all_services()
        return

    if args.status:
        show_status()
        return

    print_banner()
    ensure_studio_environment()

    procs = []

    try:
        # 1. Khởi động TTS
        if not args.studio_only:
            tts_proc = start_tts_service()
            if tts_proc:
                procs.append(tts_proc)

        # 2. Khởi động Studio
        if not args.tts_only:
            studio_proc = start_studio_service()
            if studio_proc:
                procs.append(studio_proc)

        time.sleep(2)
        show_status()

        print("""
\033[1;32m🎉 DỰ ÁN ĐÃ KHỞI CHẠY THÀNH CÔNG!\033[0m
👉 Truy cập Studio: \033[1;34mhttp://localhost:3000\033[0m
👉 Truy cập TTS:    \033[1;34mhttp://localhost:7860\033[0m

\033[1;33m💡 Nhấn Ctrl + C để dừng tất cả dịch vụ.\033[0m
""")

        # Giữ process chính chạy và lắng nghe Ctrl+C
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n🛑 Nhận tín hiệu dừng (Ctrl+C)...")
        stop_all_services()
    except Exception as e:
        print(f"❌ Lỗi khởi chạy: {e}")
        stop_all_services()


if __name__ == "__main__":
    main()
