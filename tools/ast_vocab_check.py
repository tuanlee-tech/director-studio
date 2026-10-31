#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, ast, re
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

gen_path = Path("tools/generate_script_video2.py")
tree = ast.parse(gen_path.read_text(encoding="utf-8"))

scenes = []
for node in ast.walk(tree):
    if isinstance(node, ast.Call) and getattr(node.func, "id", "") == "add_s":
        args = [arg.value for arg in node.args if isinstance(arg, ast.Constant)]
        # args: beat, type, concept, dur, nar
        if len(args) == 5:
            scenes.append({
                "beat": args[0],
                "type": args[1],
                "concept": args[2],
                "dur": args[3],
                "nar": args[4]
            })

print(f"Total scenes parsed via AST: {len(scenes)}")

all_words = set()
for i, s in enumerate(scenes):
    clean_nar = re.sub(r"[.,:;?!()'\"]", " ", s["nar"])
    for w in clean_nar.split():
        all_words.add(w.lower())

print(f"Total unique words across all 157 scenes: {len(all_words)}")
suspicious = []
for w in sorted(all_words):
    if re.search(r"(.)\1", w):
        suspicious.append(w)
print(f"Words with repeated characters: {suspicious}")

# Let's check for any words that look like typo
# E.g. ending in invalid consonants in Vietnamese: only c, ch, m, n, ng, nh, p, t
invalid_endings = []
for w in sorted(all_words):
    # strip diacritics for basic check or check endings
    # valid endings: a, ă, â, e, ê, i, o, ô, ơ, u, ư, y, c, ch, m, n, ng, nh, p, t
    # Note: 'diderot' has localized as 'đi-đơ-rô', etc.
    # Let's inspect words with non-standard endings:
    base = re.sub(r"[àáảãạăằắẳẵặâầấẩẫậeèéẻẽẹêềếểễệiìíỉĩịoòóỏõọôồốổỗộơờớởỡợuùúủũụưừứửữựyỳýỷỹỵđ]", "v", w)
    # Check if ends with b, d, f, g (not ng), h (not ch, nh), j, k, l, q, r, s, v, w, x, z
    if re.search(r"(?<!n)g$|(?<!c|n)h$|[bdfjklqrvwsxz]$", w):
        invalid_endings.append(w)

print(f"Words with unusual endings: {invalid_endings}")
