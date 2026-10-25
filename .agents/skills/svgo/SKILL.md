---
name: svgo
description: >-
  Kỹ năng thiết kế & tối ưu hóa file SVG bằng SVGO: nén path, loại bỏ metadata rác,
  chuẩn hóa viewBox="0 0 1000 1000", bảo toàn id/class để animate stroke-dashoffset và morphing trong Remotion.
---

# 📐 SVGO — Tối Ưu Hóa & Chuẩn Hóa Vector SVG Cho Motion Graphics

Tối ưu hóa và chuẩn hóa các file và đoạn mã SVG để đưa vào các component hoạt ảnh Remotion mà không bị méo hình, giật lag hay vỡ tọa độ.

## 🎯 Ứng Dụng Trong Remotion
- Chuẩn hóa các biểu tượng tài chính (Cây nợ TreeGrowth, Vòng xoáy đen Vortex, Thẻ tín dụng, Đồng xu vàng, Lá chắn bảo vệ).
- Rút gọn và làm sạch thuộc tính `d="..."` của các thẻ `<path>` để dễ dàng nội suy (morphing) hoặc vẽ nét bút dần (`strokeDashoffset`).
- Đảm bảo tỷ lệ khung hình responsive với `viewBox="0 0 1000 1000"` hoặc `viewBox="0 0 800 600"`.

## 🛠️ Bộ Quy Tắc Tối Ưu SVG Cho AI

1. **Giữ nguyên viewBox chuẩn**:
   - Luôn đặt `viewBox="0 0 1000 1000"` (hình vuông) hoặc `viewBox="0 0 1920 1080"` (chuẩn video 16:9).
   - Thêm `preserveAspectRatio="xMidYMid meet"` để căn giữa tự nhiên.
2. **Loại bỏ thẻ rác từ Illustrator/Figma**:
   - Bỏ `<metadata>`, `<defs><clipPath id="...">` không dùng đến.
   - Bỏ các thuộc tính thừa: `data-name`, `xmlns:xlink` (nếu không dùng), `xml:space`.
3. **Giữ ID và Class có nghĩa**:
   - Đặt ID rõ ràng cho từng bộ phận cần animate: `id="trunk"`, `id="branch-left"`, `id="sprout-salary"`, `id="warning-glow"`.
4. **Vẽ nét bút viền (Path Length Drawing)**:
   - Khi cần hiệu ứng vẽ nét từ 0% đến 100%:
     ```tsx
     <path
       d="M 500,900 Q 500,600 500,400..."
       fill="none"
       stroke="#EF4444"
       strokeWidth={12}
       strokeDasharray={1000}
       strokeDashoffset={interpolate(frame, [0, 45], [1000, 0], { extrapolateRight: "clamp" })}
     />
     ```

## ⚙️ Cấu Hình SVGO Tiêu Chuẩn Cho Video
```json
{
  "plugins": [
    "removeDoctype",
    "removeXMLProcInst",
    "removeComments",
    "removeMetadata",
    "removeEditorsNSData",
    "cleanupAttrs",
    "mergeStyles",
    "inlineStyles",
    "minifyStyles",
    "cleanupIds",
    "removeUselessDefs",
    {
      "name": "removeUnknownsAndDefaults",
      "params": {
        "keepDataAttrs": false
      }
    }
  ]
}
```
