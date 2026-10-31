#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, re
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

gen_path = Path("tools/generate_script_video2.py")
content = gen_path.read_text(encoding="utf-8")

for i, line in enumerate(content.splitlines()):
    if line.strip().startswith("add_s("):
        # check quotes inside narration
        # format: add_s(beat, type, concept, dur, nar)
        # We can find all string arguments in line
        # If there are inner quotes inside nar, e.g. "mình xứng đáng"
        if '"' in line:
            print(f"Line {i+1}: {line}")
