from pathlib import Path

p = Path("channels/tien-thuc-chien/template/components/DynamicGraphic.tsx")
text = p.read_text(encoding="utf-8")

# 1. Add import
if 'import { DynamicGraphicVideo2 }' not in text:
    old_import = 'import { ChartMotion } from "./ChartMotion";'
    new_import = 'import { ChartMotion } from "./ChartMotion";\nimport { DynamicGraphicVideo2 } from "./DynamicGraphicVideo2";'
    text = text.replace(old_import, new_import, 1)

# 2. Add router dispatch
router_code = '''  // Delegate to DynamicGraphicVideo2 for video #2
  if (props?.videoSlug === "lam-phat-loi-song-luong-tang-tien-mat" || props?.slug === "lam-phat-loi-song-luong-tang-tien-mat") {
    return (
      <DynamicGraphicVideo2
        title={title}
        label={label}
        description={description}
        component={component}
        scene={scene}
        theme={theme}
        durationInFrames={durationInFrames}
        props={props}
        narration={narration}
      />
    );
  }
'''

anchor = 'const animProgress = Math.min(1, Math.max(0, frame / (durationInFrames || 120)));'
if 'Delegate to DynamicGraphicVideo2' not in text and anchor in text:
    text = text.replace(anchor, anchor + "\n\n" + router_code, 1)

p.write_text(text, encoding="utf-8")
print("Successfully updated DynamicGraphic.tsx with Video 2 routing!")
