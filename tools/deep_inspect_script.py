#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/deep_inspect_script.py — Exhaustive audit of script.md
"""
import sys
import re
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

script_path = Path("channels/tien-thuc-chien/videos/lam-phat-loi-song-luong-tang-tien-mat/script.md")
content = script_path.read_text(encoding="utf-8")
blocks = re.split(r"##\s*Scene\s*(\d+)", content)

print(f"Total scenes: {len(blocks)//2}\n")

issues = []

# List of English words that Vieneu TTS will fail or stumble on:
en_words = [
    r"\bapp\b", r"\bgym\b", r"\bbluetooth\b", r"\bhedonic\b", r"\btreadmill\b",
    r"\bdiderot\b", r"\bpresent\b", r"\bbias\b", r"\bdomino\b", r"\bdopamine\b",
    r"\bauto-debit\b", r"\bauto\b", r"\bdebit\b", r"\batm\b", r"\bseal\b",
    r"\bqr\b", r"\bpost\b", r"\bcard\b", r"\bfreeze\b", r"\brule\b"
]

for i in range(1, len(blocks), 2):
    s_num = int(blocks[i])
    s_body = blocks[i+1]
    
    # Extract fields
    beat_m = re.search(r"-\s*Beat:\s*(.+)", s_body)
    type_m = re.search(r"-\s*Loại dự kiến:\s*(.+)", s_body)
    concept_m = re.search(r"-\s*Visual concept:\s*(.+)", s_body)
    dur_m = re.search(r"-\s*Duration ước tính:\s*(\d+)s", s_body)
    nar_lines = [l for l in s_body.splitlines() if l.startswith("- Narration:")]
    nar = nar_lines[0].replace("- Narration:", "").strip(" \"") if nar_lines else ""
    
    dur = int(dur_m.group(1)) if dur_m else 6
    stype = type_m.group(1).strip() if type_m else "GFX"
    concept = concept_m.group(1).strip() if concept_m else ""
    
    # Check 1: ngàn instead of nghìn
    if "ngàn" in nar.lower():
        issues.append((s_num, "Dùng 'ngàn' thay vì 'nghìn'", nar))
        
    # Check 2: English words in narration
    for pat in en_words:
        if re.search(pat, nar, re.IGNORECASE):
            issues.append((s_num, f"Từ tiếng Anh trong lời đọc ({pat.strip(chr(92)+'b')})", nar))
            
    # Check 3: Broken grammar or colloquial slang
    slang = ["cày cuốc", "mất đứt", "ngốn", "sang chảnh", "rỗng ví", "thắt lưng buộc bụng", "đốt sạch"]
    for sl in slang:
        if sl in nar.lower():
            issues.append((s_num, f"Khẩu ngữ/từ chưa chuẩn mực ('{sl}')", nar))
            
    # Check 4: Check punctuation and sentence structure
    if not nar.endswith((".", "!", "?")):
        issues.append((s_num, "Thiếu dấu kết câu", nar))
        
    # Check 5: AIV word count constraint
    if stype == "AIV":
        w_count = len(nar.split())
        max_w = {4: 12, 6: 18, 8: 24, 10: 29}.get(dur, 18)
        if w_count > max_w:
            issues.append((s_num, f"AIV quá số từ cho phép ({w_count}/{max_w})", nar))

print(f"Tổng cộng phát hiện {len(issues)} điểm cần chuẩn hóa:\n")
for iss in issues:
    print(f"[S{iss[0]:03d}] {iss[1]}:")
    print(f"       -> \"{iss[2]}\"\n")
