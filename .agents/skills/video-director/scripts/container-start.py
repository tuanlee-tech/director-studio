#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
container-start.py — Video Director Container Manager (Docker Compose Orchestrator)
Quản lý vòng đời container của project (VieNeu TTS, OpenAI Speech API, Studio UI)
Hỗ trợ tự động nhận diện phần cứng GPU/CPU và fallback thân thiện.
"""

import sys
import os
import subprocess
import shutil
import argparse
from pathlib import Path

# Fix Unicode/UTF-8 output for Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def find_project_root():
    """Tìm thư mục gốc project chứa file docker-compose.yml."""
    current = Path(__file__).resolve().parent
    for _ in range(6):
        if (current / "docker-compose.yml").is_file():
            return current
        current = current.parent
    # Fallback to current working directory
    cwd = Path.cwd()
    if (cwd / "docker-compose.yml").is_file():
        return cwd
    return Path(__file__).resolve().parent.parent.parent.parent

def check_docker_cli():
    """Kiểm tra Docker CLI có trong hệ thống không."""
    docker_bin = shutil.which("docker")
    if not docker_bin:
        return False, "Không tìm thấy lệnh 'docker' trong hệ thống (PATH)."
    
    # Kiểm tra Docker daemon có đang chạy không
    try:
        res = subprocess.run(
            ["docker", "info"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=8,
            text=True
        )
        if res.returncode != 0:
            return False, "Docker CLI có sẵn nhưng Docker daemon chưa chạy. Vui lòng khởi động Docker Desktop hoặc chạy 'sudo systemctl start docker'."
        return True, docker_bin
    except subprocess.TimeoutExpired:
        return False, "Docker daemon phản hồi quá chậm (timeout). Vui lòng kiểm tra Docker Desktop."
    except Exception as e:
        return False, f"Lỗi kiểm tra Docker daemon: {str(e)}"

def detect_hardware():
    """Phát hiện GPU NVIDIA để quyết định profile compose (gpu hoặc cpu)."""
    has_nvidia = False
    gpu_name = "None"
    
    nvidia_smi = shutil.which("nvidia-smi")
    if nvidia_smi:
        try:
            res = subprocess.run(
                ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=4,
                text=True
            )
            if res.returncode == 0 and res.stdout.strip():
                has_nvidia = True
                gpu_name = res.stdout.strip().split("\n")[0]
        except Exception:
            pass
            
    return has_nvidia, gpu_name

def action_start(root_dir, profile=None, build=False):
    print("=" * 72)
    print("🚀 KHỞI ĐỘNG CONTAINER PROJECT (AI AUDIO & VIDEO DIRECTOR)")
    print("=" * 72)
    
    docker_ok, docker_msg = check_docker_cli()
    if not docker_ok:
        print(f"\n❌ [DOCKER CHƯA SẴN SÀNG]: {docker_msg}\n")
        print("💡 GỢI Ý THAY THẾ:")
        print("  1. Khởi động Native qua Python/uv (không cần Docker):")
        print("     • Windows : gõ lệnh cheatcode '@start-tts' hoặc chạy '.\\launcher.ps1 start'")
        print("     • Linux   : gõ lệnh cheatcode '@start-tts' hoặc chạy './launcher.sh start'")
        print("  2. Nếu muốn dùng Docker:")
        print("     • Tải và cài đặt Docker Desktop: https://www.docker.com/products/docker-desktop/")
        print("     • Khởi động Docker Desktop rồi chạy lại '@start-container'\n")
        return 1

    # Quyết định profile CPU hoặc GPU
    has_gpu, gpu_name = detect_hardware()
    if not profile or profile == "auto":
        if has_gpu:
            profile = "gpu"
            print(f"🎮 Phát hiện GPU NVIDIA: {gpu_name}")
            print(f"👉 Tự động chọn Profile: 'gpu' (PyTorch + CUDA)")
        else:
            profile = "cpu"
            print("💻 Không phát hiện GPU rời. Chọn Profile: 'cpu' (ONNX Runtime nhẹ, không cần GPU)")
    else:
        profile = profile.lower()
        print(f"⚙️  Profile chỉ định: '{profile}'")

    compose_file = root_dir / "docker-compose.yml"
    if not compose_file.exists():
        print(f"❌ Không tìm thấy file docker-compose.yml tại {root_dir}")
        return 1

    cmd = ["docker", "compose", "--profile", profile, "up", "-d"]
    if build:
        cmd.append("--build")

    print(f"\n⏳ Đang thực thi: {' '.join(cmd)}")
    print("Thư mục làm việc:", str(root_dir))
    print("Vui lòng đợi trong giây lát...\n")

    try:
        res = subprocess.run(cmd, cwd=str(root_dir))
        if res.returncode != 0:
            print(f"\n❌ Khởi động container thất bại với mã lỗi {res.returncode}")
            return res.returncode
        
        print("\n" + "=" * 72)
        print("✅ KHỞI ĐỘNG CÁC CONTAINER THÀNH CÔNG!")
        print("=" * 72)
        print("📌 Danh sách dịch vụ sẵn sàng:")
        print("   • VieNeu TTS Web UI   : http://localhost:7860")
        print("   • VieNeu TTS API (V1) : http://localhost:8000 (OpenAI endpoint: /v1/audio/speech)")
        print("   • Studio Dashboard    : http://localhost:3000")
        print("\n💡 Các lệnh tiện ích:")
        print("   • Kiểm tra trạng thái : @status-container (hoặc 'docker compose ps')")
        print("   • Dừng container      : @stop-container (hoặc 'docker compose down')")
        print("=" * 72 + "\n")
        return 0
    except Exception as e:
        print(f"❌ Lỗi khi gọi docker compose: {e}")
        return 1

def action_stop(root_dir):
    print("=" * 72)
    print("🛑 DỪNG TOÀN BỘ CONTAINER PROJECT")
    print("=" * 72)
    
    docker_ok, docker_msg = check_docker_cli()
    if not docker_ok:
        print(f"❌ [LỖI DOCKER]: {docker_msg}")
        return 1

    cmd = ["docker", "compose", "--profile", "cpu", "--profile", "gpu", "down"]
    print(f"⏳ Đang thực thi: {' '.join(cmd)}")
    try:
        res = subprocess.run(cmd, cwd=str(root_dir))
        if res.returncode == 0:
            print("✅ Đã dừng toàn bộ container thành công.")
        return res.returncode
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return 1

def action_status(root_dir):
    print("=" * 72)
    print("📊 TRẠNG THÁI CONTAINER PROJECT")
    print("=" * 72)
    
    docker_ok, docker_msg = check_docker_cli()
    if not docker_ok:
        print(f"⚠️ [DOCKER]: {docker_msg}")
        return 1

    cmd = ["docker", "compose", "--profile", "cpu", "--profile", "gpu", "ps"]
    try:
        subprocess.run(cmd, cwd=str(root_dir))
        return 0
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return 1

def main():
    parser = argparse.ArgumentParser(description="Quản lý container project qua Docker Compose.")
    parser.add_argument("action", nargs="?", default="start", choices=["start", "stop", "status", "down", "up", "ps"],
                        help="Hành động: start (up), stop (down), status (ps)")
    parser.add_argument("--profile", choices=["cpu", "gpu", "auto"], default="auto",
                        help="Profile container (cpu, gpu, hoặc auto)")
    parser.add_argument("--build", action="store_true", help="Build lại Docker image nếu có thay đổi mã nguồn")

    args = parser.parse_args()
    root_dir = find_project_root()

    action = args.action.lower()
    if action in ["start", "up"]:
        sys.exit(action_start(root_dir, profile=args.profile, build=args.build))
    elif action in ["stop", "down"]:
        sys.exit(action_stop(root_dir))
    elif action in ["status", "ps"]:
        sys.exit(action_status(root_dir))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
