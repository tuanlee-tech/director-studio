#!/usr/bin/env python3
"""
subtitle-gen.py — Sinh subtitle karaoke-style từ timing JSON files.
Sử dụng từ cheatcode @gen-subs.

Usage:
    python subtitle-gen.py <timing_dir> <output_file> [--format srt|ass|vtt] [--group-size 4]

Input: Thư mục chứa các file S###_timing.json (đọc theo thứ tự số scene)
Output: File subtitle (.srt, .ass hoặc .vtt) với karaoke timing
"""

import sys
import json
import re
import argparse
from pathlib import Path

# Fix Windows console cp1252 encoding
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def format_srt_time(ms: int) -> str:
    h = ms // 3_600_000
    m = (ms % 3_600_000) // 60_000
    s = (ms % 60_000) // 1_000
    ms_r = ms % 1_000
    return f"{h:02d}:{m:02d}:{s:02d},{ms_r:03d}"


def format_vtt_time(ms: int) -> str:
    h = ms // 3_600_000
    m = (ms % 3_600_000) // 60_000
    s = (ms % 60_000) // 1_000
    ms_r = ms % 1_000
    return f"{h:02d}:{m:02d}:{s:02d}.{ms_r:03d}"


def load_timing_files(timing_dir: str):
    """Đọc và sort các file timing JSON theo số scene."""
    dir_path = Path(timing_dir)
    files = sorted(dir_path.glob("S*_timing.json"), key=lambda p: p.name)
    if not files:
        print(f"⚠️  Không tìm thấy file *_timing.json trong: {timing_dir}")
    return files


def generate_srt(timing_files: list, group_size: int = 4) -> str:
    """Sinh nội dung file .srt karaoke."""
    lines = []
    index = 1
    offset_ms = 0

    for tf in timing_files:
        with open(tf, "r", encoding="utf-8") as f:
            data = json.load(f)

        words = data.get("words", [])
        duration_ms = data.get("duration_ms", 0)

        if not words:
            offset_ms += duration_ms
            continue

        for i in range(0, len(words), group_size):
            group = words[i : i + group_size]
            start = format_srt_time(group[0]["start_ms"] + offset_ms)
            end = format_srt_time(group[-1]["end_ms"] + offset_ms)
            text = " ".join(w["word"] for w in group)
            lines.append(f"{index}\n{start} --> {end}\n{text}\n")
            index += 1

        offset_ms += duration_ms

    return "\n".join(lines)


def generate_ass(timing_files: list, group_size: int = 4) -> str:
    """Sinh nội dung file .ass với karaoke highlight (\\k tag)."""
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
Collisions: Normal

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,Strikeout,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Default,Arial,72,&H00FFFFFF,&H0000FFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,1,2,10,10,80,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""

    def ass_time(ms: int) -> str:
        h = ms // 3_600_000
        m = (ms % 3_600_000) // 60_000
        s = (ms % 60_000) // 1_000
        cs = (ms % 1_000) // 10
        return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

    dialogues = []
    offset_ms = 0

    for tf in timing_files:
        with open(tf, "r", encoding="utf-8") as f:
            data = json.load(f)
        words = data.get("words", [])
        duration_ms = data.get("duration_ms", 0)

        if not words:
            offset_ms += duration_ms
            continue

        for i in range(0, len(words), group_size):
            group = words[i : i + group_size]
            start = ass_time(group[0]["start_ms"] + offset_ms)
            end = ass_time(group[-1]["end_ms"] + offset_ms)

            # Build \k tagged text (centiseconds per word)
            parts = []
            for w in group:
                dur_cs = (w["end_ms"] - w["start_ms"]) // 10
                parts.append(f"{{\\k{dur_cs}}}{w['word']}")
            text = " ".join(parts)
            dialogues.append(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}")

        offset_ms += duration_ms

    return header + "\n".join(dialogues) + "\n"


def generate_vtt(timing_files: list, group_size: int = 4) -> str:
    """Sinh nội dung file .vtt (WebVTT)."""
    lines = ["WEBVTT\n"]
    index = 1
    offset_ms = 0

    for tf in timing_files:
        with open(tf, "r", encoding="utf-8") as f:
            data = json.load(f)
        words = data.get("words", [])
        duration_ms = data.get("duration_ms", 0)

        if not words:
            offset_ms += duration_ms
            continue

        for i in range(0, len(words), group_size):
            group = words[i : i + group_size]
            start = format_vtt_time(group[0]["start_ms"] + offset_ms)
            end = format_vtt_time(group[-1]["end_ms"] + offset_ms)
            text = " ".join(w["word"] for w in group)
            lines.append(f"{index}\n{start} --> {end}\n{text}\n")
            index += 1

        offset_ms += duration_ms

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Sinh subtitle karaoke từ timing JSON")
    parser.add_argument("timing_dir", help="Thư mục chứa file *_timing.json")
    parser.add_argument("output_file", help="Đường dẫn file subtitle đầu ra")
    parser.add_argument("--format", default="srt", choices=["srt", "ass", "vtt"],
                        help="Định dạng output (mặc định: srt)")
    parser.add_argument("--group-size", type=int, default=4,
                        help="Số từ mỗi dòng subtitle (mặc định: 4)")
    args = parser.parse_args()

    timing_files = load_timing_files(args.timing_dir)
    if not timing_files:
        sys.exit(1)

    print(f"📝 Đang tạo subtitle [{args.format}] từ {len(timing_files)} scene(s)...")

    if args.format == "srt":
        content = generate_srt(timing_files, args.group_size)
    elif args.format == "ass":
        content = generate_ass(timing_files, args.group_size)
    else:
        content = generate_vtt(timing_files, args.group_size)

    output_path = Path(args.output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")

    print(f"✅ Subtitle saved: {args.output_file}")


if __name__ == "__main__":
    main()
