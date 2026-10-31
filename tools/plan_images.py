#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, re
from pathlib import Path

scenes = json.loads(Path("tools/img_scenes_list.json").read_text(encoding="utf-8"))
print(f"Total IMG scenes: {len(scenes)}")

# Map each scene to a pose and background palette
# Available poses: master_anchor (for host), thinking, stress, shock, confident, celebrating, pointing, stop, warning, holding_card, cutting, character_tai
poses_map = {}
for s in scenes:
    c = s["concept"].lower()
    sid = s["sid"]
    if "mc" in c or "anchor" in c or sid in ["S008", "S116", "S151", "S157"]:
        pose = "master_anchor"
    elif any(k in c for k in ["ăn mừng", "vui vẻ", "hạnh phúc", "nâng ly", "tự hào", "thảnh thơi", "thành đạt"]):
        pose = "celebrating" if sid in ["S002"] else "confident"
    elif any(k in c for k in ["sốc", "thẫn thờ", "bất an", "lo lắng", "ôm đầu", "ôm trán", "căng thẳng", "sợ hãi"]):
        pose = "stress" if any(k in c for k in ["ôm đầu", "ôm trán", "căng thẳng"]) else "shock"
    elif any(k in c for k in ["chặn", "từ chối", "cấm", "dừng"]):
        pose = "stop"
    elif any(k in c for k in ["cảnh báo", "nguy hiểm", "chuông"]):
        pose = "warning"
    elif any(k in c for k in ["suy ngẫm", "nhìn", "tính toán", "ngẫm", "đăm chiêu", "tần ngần"]):
        pose = "thinking"
    elif any(k in c for k in ["chỉ tay", "hướng dẫn", "mở ra"]):
        pose = "pointing"
    elif any(k in c for k in ["thẻ", "quẹt"]):
        pose = "holding_card"
    else:
        pose = "confident"
    poses_map[sid] = pose

print("Sample pose mapping:")
for sid in list(poses_map.keys())[:15]:
    print(f"  {sid}: {poses_map[sid]}")
