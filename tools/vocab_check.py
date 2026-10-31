#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scan every single word across all narrations to see all distinct words.
Check for any non-standard Vietnamese syllables or potential typos.
"""
import sys, re
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

gen_path = Path("tools/generate_script_video2.py")
content = gen_path.read_text(encoding="utf-8")

# Extract all narration strings
narrations = re.findall(r"add_s\([^,]+,\s*[^,]+,\s*[^,]+,\s*[^,]+,\s*'(.*?)'\)", content)

print(f"Total narrations found: {len(narrations)}")

all_words = set()
for nar in narrations:
    # clean punctuation
    clean_nar = re.sub(r"[.,:;?!()'\"]", " ", nar)
    for w in clean_nar.split():
        all_words.add(w.lower())

print(f"Total distinct words: {len(all_words)}")
# Print any words that look suspicious (e.g. have double vowels in weird positions, no tone, etc.)
suspicious = []
for w in sorted(all_words):
    # Check if word has repeated characters like 'aa', 'ee', 'oo' that aren't typical (in vn 'oo' is in xoong, coong)
    if re.search(r"(.)\1", w):
        suspicious.append(w)

print("Words with repeated characters:", suspicious)
