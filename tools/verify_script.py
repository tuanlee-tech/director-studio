#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/verify_script.py — Verify script constraints
"""
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
script_path = ROOT_DIR / "channels" / "tien-thuc-chien" / "videos" / "lam-phat-loi-song-luong-tang-tien-mat" / "script.md"

content = script_path.read_text(encoding="utf-8")
scenes = re.split(r"## Scene \d+", content)[1:]

print(f"Total scenes: {len(scenes)}")

all_aiv_ok = True
for idx, s in enumerate(scenes, 1):
    if "Loại dự kiến: AIV" in s:
        dur_m = re.search(r"Duration ước tính: (\d+)s", s)
        dur = int(dur_m.group(1)) if dur_m else 0
        nar_lines = [l for l in s.splitlines() if l.startswith("- Narration:")]
        nar = nar_lines[0].replace("- Narration:", "").strip(" \"") if nar_lines else ""
        w_count = len(nar.split())
        max_w = {4: 12, 6: 18, 8: 24, 10: 29}.get(dur, 18)
        ok = w_count <= max_w
        if not ok:
            all_aiv_ok = False
        print(f"Scene {idx:03d} (AIV {dur}s): {w_count}/{max_w} words -> {'PASS' if ok else 'FAIL'}")

print(f"\nAll AIV word constraints: {'PASS' if all_aiv_ok else 'FAIL'}")
