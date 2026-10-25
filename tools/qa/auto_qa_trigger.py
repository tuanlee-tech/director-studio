#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
auto_qa_trigger.py — Automated QA Trigger & Remotion Render Orchestrator
Tự động kích hoạt bộ kiểm định chất lượng (AssetQAVerifier) ngay khi quá trình tạo assets hoàn tất.
• Nếu QA [PASS] 100%: Tự động kích hoạt render Remotion video (remotion-render.py).
• Nếu QA [FAIL]: Dừng render lập tức, xuất bảng báo cáo chi tiết để sửa lỗi.
"""

import sys
import os
import json
import subprocess
import argparse
from pathlib import Path
from typing import Optional

# Reconfigure stdout for UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Ensure tools package is in sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.qa.asset_qa_verifier import AssetQAVerifier, QAReport, find_project_root


def find_render_script(root_dir: Path) -> Optional[Path]:
    """Tìm file remotion-render.py trong workspace."""
    candidates = [
        root_dir / ".agents" / "skills" / "video-director" / "scripts" / "remotion-render.py",
        root_dir / "tools" / "remotion-render.py",
        root_dir / "tools" / "remotion_render.py",
    ]
    for c in candidates:
        if c.is_file():
            return c
    return None


def run_auto_qa_trigger(
    channel: str = "tien-thuc-chien",
    slug: str = "thoat-bay-no-the-tin-dung",
    auto_render: bool = True,
    frames: Optional[str] = None,
    quality: str = "1080p",
    dry_run: bool = False,
    skip_ocr: bool = False
) -> bool:
    """
    Thực thi chu trình Auto-QA Trigger:
    1. Chạy AssetQAVerifier
    2. Nếu đạt [PASS] 100% -> Tự động kích hoạt remotion-render.py
    3. Nếu [FAIL] -> Dừng pipeline, in báo cáo chi tiết
    """
    root_dir = find_project_root()
    print("\n" + "=" * 80)
    print("🚀 KÍCH HOẠT AUTO-QA TRIGGER PIPELINE")
    print(f"   Kênh: {channel} | Video: {slug} | Tự động Render: {auto_render}")
    print("=" * 80)

    # Bước 1: Khởi chạy bộ kiểm định QA
    verifier = AssetQAVerifier(channel=channel, slug=slug, root_dir=root_dir, skip_ocr=skip_ocr)
    report: QAReport = verifier.run_all_checks()

    # Bước 2: Đánh giá kết quả
    if not report.passed:
        print("\n" + "!" * 80)
        print("🚨 [AUTO-QA TRIGGER: DỪNG RENDER] PHÁT HIỆN LỖI VI PHẠM TRONG BỘ KIỂM ĐỊNH!")
        print(f"   Có {report.failed_checks}/{report.total_checks} tiêu chuẩn kiểm định không đạt.")
        print("   Quá trình Render Remotion bị HỦY BỎ để tránh xuất bản video lỗi.")
        print(f"   Báo cáo chi tiết đã được lưu tại:")
        print(f"   📁 {verifier.reports_dir / 'qa_audit_report.md'}")
        print("!" * 80 + "\n")
        return False

    print("\n" + "=" * 80)
    print("🎉 [AUTO-QA TRIGGER: PASS 100%] TẤT CẢ TIÊU CHUẨN ĐÃ HOÀN TOÀN ĐẠT CHUẨN!")
    print("=" * 80)

    # Bước 3: Kích hoạt Render Remotion nếu được yêu cầu
    if not auto_render:
        print("ℹ️ Auto-render đang ở chế độ tắt (--no-render). Bỏ qua bước kết xuất video.")
        return True

    render_script = find_render_script(root_dir)
    if not render_script:
        print("❌ Không tìm thấy script remotion-render.py trong workspace!")
        return False

    if dry_run:
        print(f"🧪 [DRY-RUN] Giả lập kích hoạt thành công: {render_script} {slug} --channel {channel}")
        if frames:
            print(f"   Target frames: {frames}")
        return True

    print(f"\n🎬 [TỰ ĐỘNG KÍCH HOẠT RENDER REMOTION]")
    print(f"   Script : {render_script}")
    print(f"   Target : {slug} ({channel})")
    if frames:
        print(f"   Frames : {frames}")
    print("-" * 80)

    cmd = [
        sys.executable,
        str(render_script),
        slug,
        "--channel", channel,
        "--quality", quality
    ]
    if frames:
        cmd.extend(["--frames", frames])

    try:
        proc = subprocess.run(cmd, cwd=str(root_dir))
        if proc.returncode == 0:
            print("\n" + "=" * 80)
            print("🎉🎉 [RENDER HOÀN TẤT] Video Remotion đã được xuất bản thành công! 🎉🎉")
            print("=" * 80 + "\n")
            return True
        else:
            print(f"\n❌ Remotion render kết thúc với mã lỗi {proc.returncode}")
            return False
    except Exception as e:
        print(f"\n❌ Lỗi khi khởi chạy process render: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Automated QA Trigger & Remotion Render Orchestrator")
    parser.add_argument("slug", nargs="?", default="thoat-bay-no-the-tin-dung", help="Slug của video")
    parser.add_argument("--channel", default="tien-thuc-chien", help="Tên kênh (mặc định: tien-thuc-chien)")
    parser.add_argument("--no-render", action="store_true", help="Chỉ chạy QA, không tự động render")
    parser.add_argument("--frames", default=None, help="Chỉ định frames cần render (ví dụ: 0-90 để test nhanh)")
    parser.add_argument("--quality", default="1080p", choices=["720p", "1080p", "4k"], help="Độ phân giải")
    parser.add_argument("--dry-run", action="store_true", help="Chạy giả lập không render thực tế")
    parser.add_argument("--skip-ocr", action="store_true", help="Bỏ qua quét RapidOCR để tăng tốc độ kiểm thử")

    args = parser.parse_args()

    success = run_auto_qa_trigger(
        channel=args.channel,
        slug=args.slug,
        auto_render=not args.no_render,
        frames=args.frames,
        quality=args.quality,
        dry_run=args.dry_run,
        skip_ocr=args.skip_ocr
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
