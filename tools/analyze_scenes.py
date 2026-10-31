#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, re, json
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

script_path = Path("channels/tien-thuc-chien/videos/lam-phat-loi-song-luong-tang-tien-mat/script.md")
content = script_path.read_text(encoding="utf-8")

blocks = re.split(r"##\s*Scene\s*(\d+)", content)
gfx_scenes = []
img_scenes = []
aiv_scenes = []

for i in range(1, len(blocks), 2):
    num = int(blocks[i])
    body = blocks[i+1]
    stype_m = re.search(r"-\s*Loại dự kiến:\s*(.+)", body)
    stype = stype_m.group(1).strip() if stype_m else "GFX"
    concept_m = re.search(r"-\s*Visual concept:\s*(.+)", body)
    concept = concept_m.group(1).strip() if concept_m else ""
    nar_m = re.search(r'-\s*Narration:\s*"([^"]+)"', body)
    nar = nar_m.group(1).strip() if nar_m else ""

    item = {"num": num, "sid": f"S{num:03d}", "type": stype, "concept": concept, "nar": nar}
    if stype == "GFX":
        gfx_scenes.append(item)
    elif stype == "IMG":
        img_scenes.append(item)
    elif stype == "AIV":
        aiv_scenes.append(item)

print(f"Total scenes: {len(gfx_scenes) + len(img_scenes) + len(aiv_scenes)}")
print(f"GFX scenes: {len(gfx_scenes)}")
print(f"IMG scenes: {len(img_scenes)}")
print(f"AIV scenes: {len(aiv_scenes)}")

with open("tools/gfx_scenes_list.json", "w", encoding="utf-8") as f:
    json.dump(gfx_scenes, f, ensure_ascii=False, indent=2)

with open("tools/img_scenes_list.json", "w", encoding="utf-8") as f:
    json.dump(img_scenes, f, ensure_ascii=False, indent=2)

print("Saved gfx_scenes_list.json and img_scenes_list.json")
