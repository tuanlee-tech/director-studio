import sys
from pathlib import Path
from rapidocr_onnxruntime import RapidOCR

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

engine = RapidOCR()
assets_dir = Path(r"channels/tien-thuc-chien/videos/thoat-bay-no-the-tin-dung/assets")

png_files = sorted(list(assets_dir.glob("*.png")))
print(f"Bắt đầu quét OCR trên {len(png_files)} file PNG...")

tainted_files = []
clean_files = []

for p in png_files:
    result, _ = engine(str(p))
    texts = [item[1] for item in result] if result else []
    full_text = " ".join(texts)
    
    # Check if filename or scene code or 'Rename' is in text
    scene_code = p.stem.split("-")[0]
    has_filename_leak = (
        scene_code in full_text or 
        ".png" in full_text.lower() or 
        "rename" in full_text.lower() or 
        "scene" in full_text.lower() or
        "img" in full_text.lower() or
        "aiv" in full_text.lower()
    )
    
    if has_filename_leak or len(texts) > 0:
        print(f"\n❌ [{p.name}] Phát hiện text ({len(texts)} cụm):")
        for t in texts:
            print(f"    - {t}")
        if has_filename_leak:
            tainted_files.append((p.name, texts))
        else:
            # Has some text, might be background signs or branding
            print(f"    ℹ️ (Text nền/branding, không phải filename leak)")
            clean_files.append(p.name)
    else:
        print(f"✅ [{p.name}] Sạch, không có text")
        clean_files.append(p.name)

print("\n" + "="*60)
print(f"TỔNG KẾT:")
print(f"• Số ảnh bị dán text/filename: {len(tainted_files)}")
print(f"• Số ảnh sạch: {len(clean_files)}")
print("Danh sách ảnh bị lỗi text dán vào:")
for f, txts in tainted_files:
    print(f"  - {f}: {txts[:3]}")
