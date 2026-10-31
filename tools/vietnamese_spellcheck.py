#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/vietnamese_spellcheck.py — Scan script.md for invalid syllables or typos
"""
import sys
import re
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

content = Path("channels/tien-thuc-chien/videos/lam-phat-loi-song-luong-tang-tien-mat/script.md").read_text(encoding="utf-8")

# Extract only Vietnamese words
words = re.findall(r"[a-zA-ZÀ-ỹà-ỹ0-9%_-]+", content)
unique_words = sorted(list(set(words)))

# Find words with suspicious characters, weird vowels or invalid combinations
suspicious = []
for w in unique_words:
    lw = w.lower()
    # Check for duplicate vowels like "aạ", "eé", "oò" etc.
    if re.search(r"([aăâeêioôơuưy])\1", lw) and lw not in ["oo", "ee"]:
        suspicious.append((w, "Lặp nguyên âm lạ"))
    # Check for invalid consonant clusters in Vietnamese
    if re.search(r"[bcdfghjklmnpqrstvwxz]{4,}", lw):
        suspicious.append((w, "Cụm phụ âm quá dài"))

print(f"Total unique tokens: {len(unique_words)}")
print(f"Suspicious tokens found: {len(suspicious)}")
for s in suspicious:
    print(f" - {s[0]}: {s[1]}")
