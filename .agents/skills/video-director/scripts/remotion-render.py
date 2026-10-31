#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
remotion-render.py — CLI Video Renderer for Video Director Skill
Gọi Remotion CLI để render video hoàn chỉnh từ remotion-composition.json.
Hỗ trợ cross-platform (Windows / Linux).
"""

import sys
import os
import json
import subprocess
import shutil
import re
import argparse
from pathlib import Path

# Fix Unicode on Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def find_project_root():
    current = Path(__file__).resolve().parent
    for _ in range(6):
        if (current / "docker-compose.yml").is_file():
            return current
        current = current.parent
    return Path.cwd()

def resolve_active_video(root_dir, channel=None, slug=None):
    channels_dir = root_dir / "channels"
    active_channel = channel

    # Nếu có slug nhưng chưa có channel, tự quét tìm kênh chứa slug này
    if slug and not active_channel and channels_dir.exists():
        for c in channels_dir.iterdir():
            if c.is_dir() and (c / "videos" / slug).exists():
                active_channel = c.name
                break

    if not active_channel:
        # Kiểm tra config trong video-director resources
        cfg_file = root_dir / ".agents" / "skills" / "video-director" / "resources" / "config.json"
        if cfg_file.exists():
            try:
                cfg = json.loads(cfg_file.read_text(encoding="utf-8"))
                val = cfg.get("active_channel")
                if val:
                    active_channel = val
            except Exception:
                pass

    if not active_channel:
        # Quét kênh đầu tiên có video trong channels/
        if channels_dir.exists():
            for c in channels_dir.iterdir():
                if c.is_dir() and not c.name.startswith("."):
                    v_dir = c / "videos"
                    if v_dir.exists() and any(v.is_dir() for v in v_dir.iterdir()):
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

def main():
    parser = argparse.ArgumentParser(description="Render video MP4 tự động bằng Remotion Engine.")
    parser.add_argument("slug", nargs="?", default=None, help="Slug của video (ví dụ: thoat-bay-no-the-tin-dung)")
    parser.add_argument("--channel", default=None, help="Tên kênh (mặc định lấy active channel)")
    parser.add_argument("--frames", default=None, help="Chỉ định frames cần render (ví dụ: 0-90 để test nhanh)")
    parser.add_argument("--quality", default="1080p", choices=["720p", "1080p", "4k"], help="Độ phân giải")

    args = parser.parse_args()
    root_dir = find_project_root()
    channel, slug = resolve_active_video(root_dir, args.channel, args.slug)

    video_dir = root_dir / "channels" / channel / "videos" / slug
    comp_file = video_dir / "assets" / "remotion-composition.json"
    remotion_dir = root_dir / "studio" / "remotion"
    output_file = video_dir / "final_video.mp4"

    print("=" * 72)
    print("🎬 REMOTION VIDEO RENDERER — XUẤT VIDEO TỰ ĐỘNG BẰNG CODE")
    print(f"   Kênh: {channel} | Video: {slug}")
    print("=" * 72)

    if not comp_file.exists():
        print(f"❌ Không tìm thấy composition JSON tại: {comp_file}")
        print("💡 Hãy chạy '@gen-remotion' trước để tạo file cấu hình render.")
        sys.exit(1)

    if not remotion_dir.exists():
        print(f"❌ Không tìm thấy thư mục Remotion tại: {remotion_dir}")
        sys.exit(1)

    # Đọc dữ liệu composition
    try:
        comp_data = json.loads(comp_file.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"❌ Lỗi đọc file composition: {e}")
        sys.exit(1)

    temp_props = remotion_dir / f"temp_props_{slug}.json"
    temp_props.write_text(json.dumps(comp_data, ensure_ascii=False), encoding="utf-8")

    # Clean up old output or leftover progress files to avoid Windows NTFS EPERM rename issue
    if output_file.exists():
        try:
            output_file.unlink()
        except Exception as e:
            try:
                subprocess.run(["powershell", "-Command", f"Remove-Item -Path '{output_file}' -Force"], check=False)
            except Exception:
                print(f"⚠️ Không thể xóa file video cũ: {e}")

    for prog_file in video_dir.glob("*.remotion-in-progress"):
        try:
            prog_file.unlink()
        except Exception:
            try:
                subprocess.run(["powershell", "-Command", f"Remove-Item -Path '{prog_file}' -Force"], check=False)
            except Exception:
                pass

    cmd = [
        "npx", "remotion", "render",
        "src/index.ts", "MainVideo",
        str(output_file),
        f"--props={temp_props.name}",
        "--overwrite",
        "--gl=angle",
        "--concurrency=6",
        "--timeout=60000"
    ]

    if args.frames:
        cmd.append(f"--frames={args.frames}")

    print(f"⏳ Bắt đầu render Remotion...")
    print(f"📁 Output: {output_file}")
    if args.frames:
        print(f"🎯 Target frames: {args.frames}")
    print("-" * 72)

    shell_needed = sys.platform == "win32"
    try:
        proc = subprocess.Popen(
            cmd,
            cwd=str(remotion_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            shell=shell_needed,
            encoding="utf-8",
            errors="replace"
        )

        progress_pattern = re.compile(r"Rendered\s+(\d+)/(\d+)")
        percent_pattern = re.compile(r"(\d+)%")

        for line in iter(proc.stdout.readline, ""):
            line_str = line.strip()
            if not line_str:
                continue

            prog_match = progress_pattern.search(line_str)
            if prog_match:
                curr, total = int(prog_match.group(1)), int(prog_match.group(2))
                if curr % 50 == 0 or curr == total:
                    pct = int((curr / total) * 100) if total > 0 else 0
                    bar = "█" * (pct // 5) + "░" * (20 - (pct // 5))
                    print(f"\r  [{bar}] {pct}% ({curr}/{total} frames) ", end="", flush=True)
            elif "Rendered" in line_str or ("Bundling" in line_str and "%" in line_str):
                pass
            else:
                print(f"\n  {line_str}")

        proc.wait()
        print("\n" + "-" * 72)

        if temp_props.exists():
            try:
                temp_props.unlink()
            except Exception:
                pass

        if proc.returncode == 0 and output_file.exists():
            size_mb = output_file.stat().st_size / (1024 * 1024)
            print("=" * 72)
            print("🎉 XUẤT VIDEO MP4 THÀNH CÔNG!")
            print(f"   • File xuất bản : {output_file}")
            print(f"   • Kích thước     : {size_mb:.2f} MB")
            print(f"   • Chuẩn mã hóa  : H.264 / AAC (1080p 30fps)")
            print(f"   • Xem trước web : http://localhost:3000 (Tab Video Preview)")
            print("=" * 72)
            sys.exit(0)
        else:
            print(f"❌ Render thất bại với exit code {proc.returncode}")
            sys.exit(proc.returncode)
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        if temp_props.exists():
            try:
                temp_props.unlink()
            except Exception:
                pass
        sys.exit(1)

if __name__ == "__main__":
    main()
