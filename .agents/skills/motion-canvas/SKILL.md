---
name: motion-canvas
description: >-
  Kỹ năng hoạt ảnh giải thích toán học theo phong cách Motion Canvas: Đồ thị hàm số,
  đường cong spline, minh họa công thức lãi kép (Compound Interest) và chu kỳ 45 ngày bằng vector hình học chuẩn mực.
---

# 📐 Motion Canvas — Hoạt Ảnh Giải Thích Khoa Học & Toán Học Bằng TypeScript

Motion Canvas đại diện cho triết lý đồ họa giải thích (Visual Explainer): Minh họa các khái niệm trừu tượng (như Lãi kép, Vòng xoáy nợ, Dòng tiền chiết khấu) bằng các đường cong hình học, tọa độ chính xác và biểu đồ hàm số biến thiên liên tục.

## 🎯 Ứng Dụng Trong Video Tài Chính
- **Vẽ đường cong Lãi Kép hàm mũ ($e^{rt}$)**: Minh họa cách khoản nợ nhỏ bùng nổ theo cấp số nhân sau 12 tháng.
- **Trục thời gian lùi ngược 45 ngày**: Mũi tên cong trượt ngược từ ngày sao kê về ngày giao dịch đầu tiên.
- **Biểu đồ Venn / Ma trận phân loại tài chính**: Phân chia chi tiêu thiết yếu vs chi tiêu bốc đồng bằng các vòng tròn tương tác.

## ⚡ Mẫu Minh Họa Đường Cong Toán Học Trong Remotion
```tsx
import { useCurrentFrame, interpolate } from "remotion";

export const ExponentialDebtCurve = () => {
  const frame = useCurrentFrame();
  const progress = interpolate(frame, [0, 90], [0, 1], { extrapolateRight: "clamp" });

  // Tạo chuỗi điểm tọa độ đường cong hàm mũ y = x^2.5
  const points = [];
  const totalSteps = 50;
  const currentSteps = Math.floor(progress * totalSteps);

  for (let i = 0; i <= currentSteps; i++) {
    const x = 100 + (i / totalSteps) * 600;
    const normalized = i / totalSteps;
    const y = 500 - Math.pow(normalized, 2.5) * 350;
    points.push(`${x},${y}`);
  }

  const pathData = points.length > 1 ? `M ${points.join(" L ")}` : "";

  return (
    <svg viewBox="0 0 800 600" width="800" height="600">
      {/* Trục tọa độ */}
      <line x1="100" y1="500" x2="750" y2="500" stroke="#64748B" strokeWidth="4" />
      <line x1="100" y1="500" x2="100" y2="100" stroke="#64748B" strokeWidth="4" />

      {/* Đường cong hàm mũ nợ */}
      {pathData && (
        <path
          d={pathData}
          fill="none"
          stroke="#EF4444"
          strokeWidth="6"
          strokeLinecap="round"
        />
      )}

      {/* Điểm cực đại phát sáng */}
      {points.length > 0 && (
        <circle
          cx={points[points.length - 1].split(",")[0]}
          cy={points[points.length - 1].split(",")[1]}
          r="10"
          fill="#EF4444"
          filter="drop-shadow(0 0 12px #EF4444)"
        />
      )}
    </svg>
  );
};
```
