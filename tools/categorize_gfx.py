#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

scenes = json.loads(Path("tools/gfx_scenes_list.json").read_text(encoding="utf-8"))

print(f"Total GFX scenes: {len(scenes)}")
for s in scenes:
    print(f"[{s['sid']}] {s['concept']}")
