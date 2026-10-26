#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
stamp_badge_pill.py — Watermark Masking & Channel Branding Tool
Dán đè logo badge_pill.png che phủ 100% ngôi sao watermark Gemini:
- Vị trí thực tế của watermark star trên khung 1376x768: X = w - 83px, Y = h - 95px.
- Tự động scale theo tỷ lệ độ phân giải ảnh (1376x768, 1280x720, 1920x1080, 2752x1536).
- Đặt pill bao trọn tâm điểm ngôi sao: Y_pos = star_y - (badge_h // 2), X_pos = w - badge_w - 35px.
- Luôn đọc từ bản gốc trong assets/raw_backup/ để đảm bảo chất lượng và không bị dán đè nhiều lần.
- Đồng bộ tự động sang studio/remotion/public/assets/.
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
    Dán logo badge_pill.png che 100% ngôi sao watermark Gemini.
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

        # Tọa độ thực nghiệm chuẩn xác của watermark Gemini:
        # Star center: X = w - 83 * scale, Y = h - 95 * scale
        badge_w = int(260 * scale)
        badge_h = int(badge_w * (badge.height / badge.width))

        star_y = h - int(95 * scale)
        # Căn chỉnh tâm pill trùng tâm ngôi sao theo trục Y
        pos_y = star_y - (badge_h // 2)
        # Căn chỉnh lề phải gọn gàng, bao phủ hoàn toàn ngôi sao theo trục X
        pos_x = w - badge_w - int(35 * scale)

        pos = (pos_x, pos_y)
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

    # Sync badge_pill sang remotion public
    rem_badge = ROOT_DIR / "studio" / "remotion" / "public" / "images" / "badge_pill.png"
    rem_badge.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(badge_path, rem_badge)

    print("=" * 70)
    print("🏷️  TIẾN HÀNH ĐÓNG DẤU BADGE_PILL MỚI CHE WATERMARK GEMINI (STAR CENTER MASK)")
    print(f"   Kênh: {channel} | Video: {slug}")
    print(f"   Badge: {badge_path.name} ({badge_path})")
    print(f"   Tọa độ chuẩn: Star Y = h - 95px, Star X = w - 83px (Định vị trung tâm)")
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
            print(f"  ✅ Đã đóng dấu che kín watermark: {img_file.name}")

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
