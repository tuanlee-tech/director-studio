#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import re
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

script_path = Path("channels/tien-thuc-chien/videos/lam-phat-loi-song-luong-tang-tien-mat/script.md")
content = script_path.read_text(encoding="utf-8")
blocks = re.split(r"##\s*Scene\s*(\d+)", content)

print(f"Total blocks: {len(blocks)//2}")
lines = []
for i in range(1, len(blocks), 2):
    s_num = int(blocks[i])
    s_body = blocks[i+1]
    nar_lines = [l for l in s_body.splitlines() if l.startswith("- Narration:")]
    nar = nar_lines[0].replace("- Narration:", "").strip(" \"") if nar_lines else ""
    lines.append(f"S{s_num:03d}: {nar}")

Path("tools/all_narrations.txt").write_text("\n".join(lines), encoding="utf-8")
print(f"Wrote {len(lines)} lines to tools/all_narrations.txt")
