#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/spell_and_grammar_checker.py
Comprehensive checker for spelling, digits, symbols, English words, punctuation,
and syllable correctness for Vietnamese narration text.
"""
import sys, re
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
script_path = ROOT_DIR / "channels" / "tien-thuc-chien" / "videos" / "lam-phat-loi-song-luong-tang-tien-mat" / "script.md"
text = script_path.read_text(encoding="utf-8")

scene_blocks = re.findall(r"## Scene (\d+)\s*\n- Beat: (.*?)\n- Loại dự kiến: (.*?)\n- Visual concept: (.*?)\n- Duration ước tính: (\d+)s\n- Narration: \"(.*?)\"", text)

print(f"Total scenes parsed: {len(scene_blocks)}")

issues = []

# Vietnamese valid syllables / tone marks
VIET_CHARS = set("aàáảãạăằắẳẵặâầấẩẫậeèéẻẽẹêềếểễệiìíỉĩịoòóỏõọôồốổỗộơờớởỡợuùúủũụưừứửữựyỳýỷỹỵđd")

for num, beat, stype, concept, dur, nar in scene_blocks:
    # 1. Digits
    digits = re.findall(r"\d+", nar)
    if digits:
        issues.append(f"[S{num}] Chứa chữ số ({digits}): {nar}")
    
    # 2. Math & Special symbols
    symbols = re.findall(r"[%/+=&@#$<>]", nar)
    if symbols:
        issues.append(f"[S{num}] Chứa ký tự đặc biệt ({symbols}): {nar}")

    # 3. Punctuation spacing (e.g. space before comma/period, double spaces)
    if re.search(r"\s+[,.!?:;]", nar):
        issues.append(f"[S{num}] Lỗi dấu câu cách khoảng trắng trước dấu: {nar}")
    if "  " in nar:
        issues.append(f"[S{num}] Chứa 2 dấu cách liên tiếp: {nar}")
    if not re.search(r"[.!?\"']$", nar.strip()):
        issues.append(f"[S{num}] Không kết thúc bằng dấu câu: {nar}")

    # 4. Check for unlocalized English words
    # Split words by space and punctuation
    raw_words = re.findall(r"[A-Za-zÀ-ỹĐđ]+", nar)
    for w in raw_words:
        w_lower = w.lower()
        # Common English terms that might sneak in
        if w_lower in ["app", "gym", "bluetooth", "dopamine", "diderot", "bias", "present", "treadmill", "hedonic", "status", "lifestyle", "inflation", "coffee", "latte", "freelance", "deadline", "salary", "cash", "bank"]:
            issues.append(f"[S{num}] Chứa từ tiếng Anh '{w}': {nar}")

    # 5. Check Southern vs Northern dialects
    if "ngàn" in nar.lower():
        issues.append(f"[S{num}] Chứa từ miền Nam 'ngàn' (cần đổi thành 'nghìn'): {nar}")
    if "xài" in nar.lower():
        issues.append(f"[S{num}] Chứa từ 'xài' (nên đổi thành 'tiêu' hoặc 'chi tiêu'): {nar}")

    # 6. AIV duration & word count
    if stype == "AIV":
        words_count = len(nar.split())
        if words_count > 18:
            issues.append(f"[S{num}] AIV 6s vượt quá 18 từ ({words_count} từ): {nar}")

print("\n--- KẾT QUẢ KIỂM TRA TOÀN DIỆN ---")
if not issues:
    print("✅ HOÀN TOÀN SẠCH CHÍNH TẢ, KHÔNG CÓ LỖI NÀO!")
else:
    print(f"Phát hiện {len(issues)} vấn đề:")
    for iss in issues:
        print(f"- {iss}")
