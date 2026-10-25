#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
render_thumbnail.py — Xuất Thumbnail YouTube tự động với nhân vật sticker Vox Style.
Hỗ trợ Remotion Still và chống lỗi escape quote trên Windows CLI.
"""

import sys
import os
import json
import argparse
import subprocess
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def main():
    parser = argparse.ArgumentParser(description="Render Thumbnail YouTube với Remotion Still")
    parser.add_argument("--pose", default="cutting", help="Pose nhân vật: cutting, shock, confident, stress, thinking, warning, pointing, celebrating, holding_card, stop")
    parser.add_argument("--title1", default="THOÁT BẪY NỢ", help="Dòng tiêu đề 1 (Vàng)")
    parser.add_argument("--title2", default="THẺ TÍN DỤNG", help="Dòng tiêu đề 2 (Trắng)")
    parser.add_argument("--debt-start", default="40 TRIỆU", help="Mốc dư nợ ban đầu")
    parser.add_argument("--debt-target", default="0 ĐỒNG!", help="Mốc dư nợ mục tiêu")
    parser.add_argument("--time-frame", default="SAU 10 THÁNG", help="Khung thời gian")
    parser.add_argument("--badge", default="TIỀN THỰC CHIẾN • QUY TRÌNH 4 BƯỚC", help="Huy hiệu trên cùng")
    parser.add_argument("--proof", default="Áp dụng cho thu nhập 10 - 12 triệu/tháng", help="Dòng phụ chứng minh")
    parser.add_argument("--position", choices=["left", "right"], default="left", help="Vị trí nhân vật: left (mặc định) hoặc right")
    parser.add_argument("--channel", default="tien-thuc-chien", help="Tên kênh")
    parser.add_argument("--out", default=None, help="Đường dẫn file xuất ra")

    args = parser.parse_args()

    root_dir = Path(__file__).resolve().parent.parent
    remotion_dir = root_dir / "studio" / "remotion"
    
    if args.out:
        out_path = Path(args.out).resolve()
    else:
        out_path = root_dir / "channels" / args.channel / "videos" / "thoat-bay-no-the-tin-dung" / f"thumbnail_{args.pose}.png"

    import base64
    char_file = root_dir / "channels" / args.channel / "characters" / f"{args.pose}.png"
    if char_file.exists():
        encoded = base64.b64encode(char_file.read_bytes()).decode("utf-8")
        char_data_uri = f"data:image/png;base64,{encoded}"
    else:
        char_data_uri = args.pose

    props = {
        "title_line1": args.title1,
        "title_line2": args.title2,
        "character_pose": char_data_uri,
        "debt_start": args.debt_start,
        "debt_target": args.debt_target,
        "time_frame": args.time_frame,
        "badge_text": args.badge,
        "proof_text": args.proof,
        "channel_name": args.channel,
        "character_position": args.position,
    }

    temp_props = remotion_dir / f"temp_thumb_props_{os.getpid()}.json"
    temp_props.write_text(json.dumps(props, ensure_ascii=False, indent=2), encoding="utf-8")

    cmd = [
        "npx", "remotion", "still",
        "src/index.ts", "ThumbnailMaster",
        str(out_path),
        f"--props={temp_props.name}",
        "--overwrite"
    ]

    print(f"🎨 Đang xuất Thumbnail Remotion...")
    print(f"   • Pose nhân vật : {args.pose}.png")
    print(f"   • Tiêu đề       : {args.title1} {args.title2}")
    print(f"   • Đầu ra        : {out_path}")

    try:
        proc = subprocess.run(
            cmd,
            cwd=str(remotion_dir),
            shell=sys.platform == "win32",
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )

        if temp_props.exists():
            temp_props.unlink()

        if proc.returncode == 0 and out_path.exists():
            size_kb = out_path.stat().st_size / 1024
            print(f"🎉 XUẤT THUMBNAIL THÀNH CÔNG! ({size_kb:.1f} KB)")
            print(f"📁 {out_path}")
        else:
            print(f"❌ Lỗi xuất thumbnail (exit code {proc.returncode}):")
            print(proc.stderr or proc.stdout)
            sys.exit(proc.returncode)

    except Exception as e:
        if temp_props.exists():
            temp_props.unlink()
        print(f"❌ Lỗi ngoại lệ: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
