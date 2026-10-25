---
name: animejs
description: >-
  Kỹ năng hoạt ảnh với Anime.js: Vẽ nét viền vector (strokeDashoffset), biến hình SVG morphing,
  hoạt ảnh số nhảy tăng dần, và hiệu ứng vi mô siêu nhẹ không gây giật lag.
---

# 🪄 Anime.js — Hoạt Ảnh Vector Path & Micro-Interactions Siêu Nhẹ

Anime.js là thư viện hoạt ảnh JavaScript nhỏ gọn, cực kỳ xuất sắc trong việc thao tác trực tiếp với các thuộc tính SVG (vẽ đường viền `strokeDashoffset`, biến đổi hình dạng morphing `d`, xoay góc `transform-origin`).

## 🎯 Ứng Dụng Trong Remotion
- **Vẽ nhánh cây nợ (TreeGrowth)**: Vẽ từng nhánh gai nhọn từ thân chính bung ra.
- **Biến hình đồng xu thành vòng xoáy nợ (Morphing)**: Biến đổi đường nét SVG mượt mà.
- **Bộ đếm tiền VND**: Nhảy số từ 0 lên 40.000.000 VNĐ với gia tốc tự nhiên.

## ⚡ Các Kỹ Thuật Chính Trong Remotion

### 1. Vẽ Viền SVG Theo Frame (Path Stroke Drawing)
```tsx
import { useCurrentFrame, interpolate } from "remotion";

export const AnimatedPath = () => {
  const frame = useCurrentFrame();
  const totalLength = 1200; // Chiều dài path đo được

  const strokeOffset = interpolate(frame, [0, 60], [totalLength, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <svg viewBox="0 0 800 600" width="800" height="600">
      <path
        d="M 100,500 C 200,200 400,100 700,300"
        fill="none"
        stroke="#10B981"
        strokeWidth={8}
        strokeDasharray={totalLength}
        strokeDashoffset={strokeOffset}
      />
    </svg>
  );
};
```

### 2. Số Nhảy Gia Tốc (Value Easing)
```tsx
import { useCurrentFrame, interpolate, Easing } from "remotion";

export const AnimatedCounter = ({ targetValue = 40000000 }: { targetValue?: number }) => {
  const frame = useCurrentFrame();
  const currentVal = Math.round(
    interpolate(frame, [10, 70], [0, targetValue], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
      easing: Easing.out(Easing.cubic),
    })
  );

  return (
    <div style={{ fontSize: 64, fontWeight: 900, color: "#EF4444", fontFamily: "'Be Vietnam Pro', sans-serif" }}>
      {currentVal.toLocaleString("vi-VN")} đ
    </div>
  );
};
```
