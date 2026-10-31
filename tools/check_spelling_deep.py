#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import re
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

content = Path("channels/tien-thuc-chien/videos/lam-phat-loi-song-luong-tang-tien-mat/script.md").read_text(encoding="utf-8")

# Check for common Vietnamese spelling mistakes
common_typos = {
    "chắt chiu": "chắt chiu",
    "xắp xếp": "sắp xếp",
    "sắp sếp": "sắp xếp",
    "xếp đặt": "xếp đặt",
    "sơ xuất": "sơ suất",
    "sơ suất": "sơ suất",
    "dành dụm": "dành dụm",
    "giành dụm": "dành dụm",
    "dành giật": "giành giật",
    "xum xuê": "sum suê",
    "chần chừ": "chần chừ",
    "trần trừ": "chần chừ",
    "suôn sẻ": "suôn sẻ",
    "suôn xẻ": "suôn sẻ",
    "bạc mạng": "bạt mạng",
    "chuẩn xát": "chuẩn xác",
    "chính sác": "chính xác",
    "bản lĩnh": "bản lĩnh",
    "bản lỉnh": "bản lĩnh",
    "trăn trở": "trăn trở",
    "chăn chở": "trăn trở",
    "chớp nhoáng": "chớp nhoáng",
    "trớp nhoáng": "chớp nhoáng",
    "ngăn nắp": "ngăn nắp",
    "ngăn lặp": "ngăn nắp",
    "dập tắt": "dập tắt",
    "dậm tắt": "dập tắt",
    "cứu cánh": "cứu cánh",
    "chi trả": "chi trả",
    "chi chả": "chi trả",
    "nguyên vẹn": "nguyên vẹn",
    "nguyên vẹn": "nguyên vẹn",
    "thanh thản": "thanh thản",
    "thanh thản": "thanh thản"
}

# Scan every sentence in script.md
lines = content.splitlines()
issues = []
for line_no, line in enumerate(lines, 1):
    # Check repeated words (vd: "và và", "là là", "trong trong")
    dup_m = re.findall(r"\b(\w+)\s+\1\b", line, re.IGNORECASE)
    if dup_m:
        issues.append((line_no, line, f"Từ lặp lại: {dup_m}"))
    
    # Check lowercase at sentence start after period
    m_cap = re.search(r"\.\s+([a-zà-ỹ])", line)
    if m_cap:
        issues.append((line_no, line, f"Chữ thường sau dấu chấm: '{m_cap.group(1)}'"))
        
    # Check mismatched quotes or parentheses
    if line.count('"') % 2 != 0:
        issues.append((line_no, line, "Dấu ngoặc kép không cân xứng"))
    if line.count("(") != line.count(")"):
        issues.append((line_no, line, "Dấu ngoặc đơn không cân xứng"))

print(f"Phát hiện {len(issues)} vấn đề tiềm ẩn:")
for iss in issues[:30]:
    print(f"Dòng {iss[0]}: {iss[2]} -> {iss[1][:80]}")
