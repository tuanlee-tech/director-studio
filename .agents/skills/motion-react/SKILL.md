---
name: motion-react
description: >-
  Kỹ năng Motion / Framer Motion cho React: Hoạt ảnh vật lý lò xo (Spring physics),
  AnimatePresence, layout animation, danh sách trượt vào (staggerChildren), thẻ cảnh báo nảy mượt mà.
---

# 🚀 Motion / Framer Motion Cho React & Remotion

Motion (trước đây là Framer Motion) cung cấp mô hình khai báo chuyển động tự nhiên với vật lý lò xo (Spring Physics) và tự động tính toán chuyển đổi bố cục (Layout Animations).

## 🎯 Ứng Dụng Trong Remotion
- **Xuất hiện thẻ cảnh báo tài chính**: Hiệu ứng đàn hồi (bouncy card) khi thẻ nợ trồi lên.
- **Thanh tiến trình & huy hiệu**: Biến đổi độ rộng, màu sắc và độ mờ một cách tự nhiên.
- **Danh sách lời khuyên**: Các gạch đầu dòng trượt vào lần lượt (`staggerChildren`).

## ⚡ Các Pattern Chuẩn Trong Remotion

### 1. Đồng Bộ Spring Physics Với Frame
```tsx
import { useCurrentFrame, useVideoConfig, spring } from "remotion";

export const SpringCard = ({ children }: { children: React.ReactNode }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spring({
    frame,
    fps,
    config: {
      damping: 12,
      mass: 0.6,
      stiffness: 150,
    },
  });

  const translateY = spring({
    frame,
    fps,
    from: 80,
    to: 0,
    config: { damping: 14, mass: 0.8 },
  });

  return (
    <div
      style={{
        transform: `translateY(${translateY}px) scale(${scale})`,
        opacity: Math.min(1, frame / 10),
      }}
    >
      {children}
    </div>
  );
};
```

### 2. Cảnh Báo Nhấp Nháy Hào Quang Neon
```tsx
import { useCurrentFrame } from "remotion";

export const PulsingGlowBadge = ({ text }: { text: string }) => {
  const frame = useCurrentFrame();
  const pulse = Math.sin(frame / 6) * 0.4 + 0.6; // Dao động 0.2 - 1.0

  return (
    <div
      style={{
        padding: "10px 24px",
        borderRadius: "999px",
        backgroundColor: "rgba(239, 68, 68, 0.2)",
        border: `2px solid rgba(239, 68, 68, ${pulse})`,
        boxShadow: `0 0 ${pulse * 30}px rgba(239, 68, 68, 0.6)`,
        color: "#FCA5A5",
        fontWeight: 800,
        fontSize: "20px",
        letterSpacing: "1px",
      }}
    >
      {text}
    </div>
  );
};
```
