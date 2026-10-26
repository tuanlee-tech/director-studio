#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
stamp_badge_pill.py — Watermark Masking & Channel Branding Tool
Dán đè logo badge_pill.png vào góc dưới cùng bên phải (Bottom-Right) của ảnh tĩnh:
- Tọa độ ngôi sao watermark Gemini/Nano Banana: X = -41px, Y = -41px, Size = ~37px (chuẩn hóa trên khung 1376x768).
- Tự động scale tương ứng theo độ phân giải ảnh (1376x768, 1920x1080, 2752x1536).
- Che phủ 100% ngôi sao watermark, bảo vệ thương hiệu khi thực hiện Ken Burns (pan / zoom).
- Tự động sao lưu ảnh nguyên bản vào assets/raw_backup/ trước khi dán đè.
- Đồng bộ sang studio/remotion/public/assets/.
"""

import sys
import shutil
import argparse
from pathlib import Path
from PIL import Image

# Reconfigure stdout for UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent.parent


def get_badge_path(channel: str = "tien-thuc-chien") -> Path:
    badge_file = ROOT_DIR / "channels" / channel / "images" / "badge_pill.png"
    if not badge_file.exists():
        for f in ROOT_DIR.glob(f"channels/{channel}/**/badge_pill.png"):
            return f
    return badge_file


def stamp_image_with_badge(img_path: Path, badge_path: Path, raw_backup_dir: Path) -> bool:
    """
    Dán logo badge_pill.png vào góc dưới bên phải ảnh, che hoàn toàn watermark Gemini.
    """
    try:
        raw_backup_dir.mkdir(parents=True, exist_ok=True)
        backup_file = raw_backup_dir / img_path.name

        # Nếu chưa backup thì backup bản gốc
        if not backup_file.exists():
            shutil.copy2(img_path, backup_file)

        badge = Image.open(badge_path).convert("RGBA")
        img = Image.open(backup_file).convert("RGBA")

        w, h = img.size
        scale = w / 1376.0

        # Thông số định vị chính xác theo tọa độ watermark Gemini (X: -41px, Y: -41px, Star: 37px)
        badge_w = int(210 * scale)
        badge_h = int(badge_w * (badge.height / badge.width))
        margin_right = int(20 * scale)
        margin_bottom = int(18 * scale)

        pos = (w - badge_w - margin_right, h - badge_h - margin_bottom)
        resized_badge = badge.resize((badge_w, badge_h), Image.Resampling.LANCZOS)

        # Paste badge onto image using its alpha channel
        img.paste(resized_badge, pos, resized_badge)

        # Lưu lại bản đã đóng dấu
        final_img = img.convert("RGB")
        final_img.save(img_path, quality=95)
        return True
    except Exception as e:
        print(f"❌ Lỗi đóng dấu {img_path.name}: {e}")
        return False


def stamp_all_static_assets(channel: str = "tien-thuc-chien", slug: str = "thoat-bay-no-the-tin-dung"):
    video_dir = ROOT_DIR / "channels" / channel / "videos" / slug
    assets_dir = video_dir / "assets"
    raw_backup_dir = assets_dir / "raw_backup"
    remotion_public_assets = ROOT_DIR / "studio" / "remotion" / "public" / "assets"
    badge_path = get_badge_path(channel)

    if not badge_path.exists():
        print(f"❌ Không tìm thấy badge_pill.png tại: {badge_path}")
        return

    print("=" * 70)
    print("🏷️  TIẾN HÀNH ĐÓNG DẤU BADGE_PILL VÀO ẢNH TĨNH (BOTTOM-RIGHT WATERMARK MASK)")
    print(f"   Kênh: {channel} | Video: {slug}")
    print(f"   Tọa độ chuẩn hóa: X=-41px, Y=-41px (Gemini Adaptive Mask)")
    print("=" * 70)

    img_files = sorted([
        f for f in assets_dir.glob("*_IMG.png")
        if not f.name.endswith("_sb.png")
    ])

    success_count = 0
    for img_file in img_files:
        ok = stamp_image_with_badge(img_file, badge_path, raw_backup_dir)
        if ok:
            success_count += 1
            if remotion_public_assets.exists():
                shutil.copy2(img_file, remotion_public_assets / img_file.name)
            print(f"  ✅ Đã đóng dấu & che watermark: {img_file.name}")

    print("-" * 70)
    print(f"🎉 Hoàn tất! Đã đóng dấu thành công {success_count}/{len(img_files)} ảnh tĩnh.")
    print(f"📁 Bản gốc được bảo toàn tại: {raw_backup_dir}")
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description="Stamp badge_pill on static images.")
    parser.add_argument("slug", nargs="?", default="thoat-bay-no-the-tin-dung")
    parser.add_argument("--channel", default="tien-thuc-chien")
    parser.add_argument("--file", default=None, help="Đóng dấu cho 1 file cụ thể")

    args = parser.parse_args()

    if args.file:
        fpath = Path(args.file)
        if fpath.exists():
            bpath = get_badge_path(args.channel)
            raw_dir = fpath.parent / "raw_backup"
            ok = stamp_image_with_badge(fpath, bpath, raw_dir)
            if ok:
                print(f"✅ Đã đóng dấu thành công file {fpath.name}")
        else:
            print(f"❌ File không tồn tại: {args.file}")
    else:
        stamp_all_static_assets(channel=args.channel, slug=args.slug)


if __name__ == "__main__":
    main()
