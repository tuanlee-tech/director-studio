---
name: gsap-timeline
description: >-
  Kỹ năng hoạt ảnh nâng cao với GSAP Timeline: Điều phối chuỗi chuyển động phức tạp nhiều bước,
  staggered animations, relative offsets (<, +=0.2), và đồng bộ chính xác từng mili-giây với Remotion frame.
---

# ⏳ GSAP Timeline — Điều Phối Chuỗi Hoạt Ảnh Phức Tạp Nhiều Bước

GSAP Timeline là công cụ mạnh mẽ nhất để xây dựng các chuỗi chuyển động liên hoàn, nhiều giai đoạn (Choreography) mà không bị phụ thuộc vào tính toán callback lồng nhau.

## 🎯 Ứng Dụng Trong Video
- **Roadmap / Quy trình từng bước**: Bước 1 xuất hiện -> Mũi tên trỏ sang Bước 2 -> Cảnh báo nhấp nháy -> Kết quả tổng kết.
- **Biểu đồ nhiều thanh (Multi-bar Chart)**: Các cột tăng dần lần lượt theo hiệu ứng lượn sóng (`stagger`).
- **Chuyển động máy quay ảo (Virtual Camera Panning)**: Di chuyển khung nhìn qua các mốc dữ liệu.

## ⚡ Mẫu Tích Hợp GSAP Timeline Trong Remotion
```tsx
import { useCurrentFrame, useVideoConfig } from "remotion";
import { useEffect, useRef } from "react";
import gsap from "gsap";

export const MultiStepChoreography = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const containerRef = useRef<HTMLDivElement>(null);
  const tlRef = useRef<gsap.core.Timeline | null>(null);

  useEffect(() => {
    const ctx = gsap.context(() => {
      tlRef.current = gsap.timeline({ paused: true });

      tlRef.current
        // Bước 1: Thẻ xuất hiện từ dưới lên
        .from(".step-card", {
          y: 60,
          opacity: 0,
          duration: 0.8,
          ease: "back.out(1.7)",
          stagger: 0.25,
        })
        // Bước 2: Con số nhảy bùng lên
        .from(".metric-number", {
          scale: 0.2,
          opacity: 0,
          duration: 0.6,
          ease: "elastic.out(1, 0.5)",
        }, "-=0.2")
        // Bước 3: Cảnh báo đỏ phát sáng
        .to(".alert-badge", {
          backgroundColor: "#EF4444",
          boxShadow: "0 0 25px #EF4444",
          duration: 0.4,
          repeat: 2,
          yoyo: true,
        });
    }, containerRef);

    return () => ctx.revert();
  }, []);

  // Đồng bộ frame Remotion với GSAP timeline
  useEffect(() => {
    if (tlRef.current) {
      tlRef.current.seek(frame / fps);
    }
  }, [frame, fps]);

  return (
    <div ref={containerRef} style={{ display: "flex", gap: "24px" }}>
      <div className="step-card">Thẻ 1</div>
      <div className="step-card">Thẻ 2</div>
      <div className="metric-number">35%</div>
      <div className="alert-badge">Cảnh Báo</div>
    </div>
  );
};
```
