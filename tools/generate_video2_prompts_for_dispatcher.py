#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/generate_video2_prompts_for_dispatcher.py
Sinh file assets/prompts.md chuẩn cho batch_dispatcher.py (Google Flow Multi-Account CDP).
Phân bổ 76 tác vụ (69 IMG + 7 AIV Storyboard) đều qua 4 tài khoản đang Online: Account 1, 3, 4, 5.
"""

import sys
import json
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
VIDEO_DIR = ROOT_DIR / "channels" / "tien-thuc-chien" / "videos" / "lam-phat-loi-song-luong-tang-tien-mat"
BP_FILE = VIDEO_DIR / "broll-plan.json"
PROMPTS_FILE = VIDEO_DIR / "assets" / "prompts.md"

with open(BP_FILE, "r", encoding="utf-8") as f:
    bp_data = json.load(f)

scenes = bp_data.get("scenes", [])
media_scenes = [s for s in scenes if s.get("type") in ("IMG", "AIV")]

ACTIVE_ACCOUNTS = [1, 3, 4, 5]

STYLE_IMG = (
    "2D flat vector illustration: {concept}. "
    "Vyond cartoon animation style, thick clean black outlines, bold saturated colors, minimal flat shading, solid pastel backdrop. "
    "Character consistency: 27-year-old Vietnamese professional man, short neat black hair, modern glasses, wearing crisp white button-up collared shirt. "
    "Avoid text, words, labels, typography, logos, watermarks, distorted limbs."
)

STYLE_AIV_SB = (
    "2D flat vector storyboard frame: {concept}. "
    "Vyond cartoon animation style, thick clean black outlines, bold saturated colors, minimal flat shading, solid pastel backdrop. "
    "Character consistency: 27-year-old Vietnamese professional man, short neat black hair, modern glasses, wearing crisp white button-up collared shirt. "
    "Avoid text, words, labels, typography, logos, watermarks, distorted limbs."
)

lines = [
    "# Media Prompts — lam-phat-loi-song-luong-tang-tien-mat",
    "Kênh: tien-thuc-chien | Phong cách: 2D flat vector cartoon illustration, Vyond animation style | Multi-Account Google Flow CDP",
    "",
    "## Danh sách Prompts Phân bổ Multi-Account (Accounts 1, 3, 4, 5)",
    "",
    "| Account | Scene | Type | Filename | Prompt Sinh Media |",
    "| :--- | :---: | :---: | :--- | :--- |"
]

for idx, s in enumerate(media_scenes):
    acc = ACTIVE_ACCOUNTS[idx % len(ACTIVE_ACCOUNTS)]
    sid = s.get("id") or s.get("scene_id")
    stype = s.get("type")
    concept = s.get("concept", "")
    dur = 6 if stype == "AIV" else 8

    if stype == "AIV":
        # Storyboard prompt
        target_file = f"{sid}-A_{dur}s_AIV_sb.png"
        prompt = STYLE_AIV_SB.format(concept=concept)
        lines.append(f"| **Account {acc}** | `{sid}` | AIV_SB | `{target_file}` | {prompt} |")
    else:
        target_file = f"{sid}-A_{dur}s_IMG.png"
        prompt = STYLE_IMG.format(concept=concept)
        lines.append(f"| **Account {acc}** | `{sid}` | IMG | `{target_file}` | {prompt} |")

PROMPTS_FILE.write_text("\n".join(lines), encoding="utf-8")
print(f"✅ Đã ghi hoàn tất {len(media_scenes)} tasks vào {PROMPTS_FILE}")
