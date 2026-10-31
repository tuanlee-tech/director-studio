import json, re
from pathlib import Path

p = Path("channels/tien-thuc-chien/template/components/DynamicGraphicVideo2.tsx")
text = p.read_text(encoding="utf-8")
scenes = re.findall(r'sc === "(S\d+)"', text)
print(f"Total scenes in DynamicGraphicVideo2.tsx: {len(scenes)}")

all_gfx = [s["sid"] for s in json.loads(Path("tools/gfx_scenes_list.json").read_text(encoding="utf-8"))]
missing = [s for s in all_gfx if s not in scenes]
print(f"Missing GFX scenes: {len(missing)}")
if missing:
    print(f"Details: {missing}")
else:
    print("🎉 100% GFX SCENES COVERED IN DynamicGraphicVideo2.tsx!")
