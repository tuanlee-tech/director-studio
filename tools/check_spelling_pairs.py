#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/check_spelling_pairs.py
Check known Vietnamese confusion pairs in script.md
"""
import sys
import re
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

content = Path("channels/tien-thuc-chien/videos/lam-phat-loi-song-luong-tang-tien-mat/script.md").read_text(encoding="utf-8")

# Common Vietnamese typo pairs: {wrong: right}
typo_map = {
    # s vs x
    r"\bxơ suất\b": "sơ suất",
    r"\bsơ xuất\b": "sơ suất",
    r"\bxuất sắc\b": "xuất sắc",
    r"\bsuất sắc\b": "xuất sắc",
    r"\bxắp xếp\b": "sắp xếp",
    r"\bsắp sếp\b": "sắp xếp",
    r"\bsum suê\b": "sum suê",
    r"\bxum xuê\b": "sum suê",
    r"\bsuôn sẻ\b": "suôn sẻ",
    r"\bsuôn xẻ\b": "suôn sẻ",
    r"\bxuôn xẻ\b": "suôn sẻ",
    r"\bsáng lạn\b": "xán lạn",
    r"\bxán lạng\b": "xán lạn",
    r"\bsơ sài\b": "sơ sài",
    r"\bxơ xài\b": "sơ sài",
    r"\bchắt chiu\b": "chắt chiu",
    r"\btrắt chiu\b": "chắt chiu",
    r"\bchắt bóp\b": "chắt bóp",
    r"\bchần chừ\b": "chần chừ",
    r"\btrần trừ\b": "chần chừ",
    r"\btrăn trở\b": "trăn trở",
    r"\bchăn chở\b": "trăn trở",
    r"\btrôi tuột\b": "trôi tuột",
    r"\bchôi tuột\b": "trôi tuột",
    r"\bdành dụm\b": "dành dụm",
    r"\bgiành dụm\b": "dành dụm",
    r"\bgiữ gìn\b": "giữ gìn",
    r"\bdữ dìn\b": "giữ gìn",
    r"\brò rỉ\b": "rò rỉ",
    r"\bdò dỉ\b": "rò rỉ",
    r"\brỗng không\b": "rỗng không",
    r"\brỗng tuếch\b": "rỗng tuếch",
    r"\bgiật gấu vá vai\b": "giật gấu vá vai",
    r"\bdật gấu vá vai\b": "giật gấu vá vai",
    r"\bvỡ trận\b": "vỡ trận",
    r"\bvở trận\b": "vỡ trận",
    r"\btrả góp\b": "trả góp",
    r"\bchả góp\b": "trả góp",
    r"\bbất khả xâm phạm\b": "bất khả xâm phạm",
    r"\bbất khả xâm phạm\b": "bất khả xâm phạm",
    r"\bcắt đứt\b": "cắt đứt",
    r"\bcắt đức\b": "cắt đứt",
    r"\bbứt phá\b": "bứt phá",
    r"\bbức phá\b": "bứt phá",
    r"\bchững lại\b": "chững lại",
    r"\bchửng lại\b": "chững lại",
    r"\bcứu cánh\b": "cứu cánh",
    r"\btích sản\b": "tích sản",
    r"\btích sãn\b": "tích sản",
    r"\blãi kép\b": "lãi kép",
    r"\blãi suất\b": "lãi suất",
    r"\blãi xuất\b": "lãi suất",
    r"\bxuất hiện\b": "xuất hiện",
    r"\bsuất hiện\b": "xuất hiện",
    r"\bchi phí\b": "chi phí",
    r"\bquy trình\b": "quy trình",
    r"\bqui trình\b": "quy trình",
}

found_typos = []
for wrong_pat, correct in typo_map.items():
    matches = re.findall(wrong_pat, content, re.IGNORECASE)
    if matches and wrong_pat.strip(r"\b") != correct:
        found_typos.append((wrong_pat, correct, len(matches)))

print(f"Known typo scan: {len(found_typos)} issues found.")
for ft in found_typos:
    print(f" - Found '{ft[0]}' -> Should be '{ft[1]}' ({ft[2]} occurrences)")
