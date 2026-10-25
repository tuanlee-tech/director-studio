---
name: gsap-skill
description: >-
  Official GreenSock GSAP animation skills: Core tweens (to, from, fromTo), timelines,
  plugins (Flip, MotionPath, ScrollTrigger), React integration, stagger, and smooth frame-based syncing.
---

# ⚡ GSAP Skill (Official greensock/gsap-skills)

Bộ kỹ năng chính thức từ GreenSock hướng dẫn AI lập trình animation GSAP chuẩn mực cho React và Remotion.

## 📌 Các Module Chi Tiết

- **[GSAP Core](./gsap-core/SKILL.md)**: `gsap.to()`, `gsap.from()`, `gsap.fromTo()`, easing functions, durations, staggers, defaults.
- **[GSAP Timeline](./gsap-timeline/SKILL.md)**: Chuỗi hoạt cảnh tuần tự, relative offsets (`<`, `+=0.2`), labels.
- **[GSAP React Integration](./gsap-react/SKILL.md)**: `useGSAP` hook, scoping refs, cleanup, context.
- **[GSAP Plugins](./gsap-plugins/SKILL.md)**: TextPlugin, MotionPathPlugin, MorphSVGPlugin, Flip.
- **[GSAP Performance](./gsap-performance/SKILL.md)**: GPU acceleration (`transform`, `opacity`), tránh layout thrashing.
- **[GSAP Utils](./gsap-utils/SKILL.md)**: `gsap.utils.clamp()`, `gsap.utils.mapRange()`, `gsap.utils.interpolate()`.

## ⏱️ Đồng Bộ GSAP với Remotion Frame

Trong Remotion, timeline GSAP phải được tạm dừng (`paused: true`) và cập nhật thời gian theo frame của video:
```tsx
import { useCurrentFrame, useVideoConfig } from "remotion";
import { useEffect, useRef } from "react";
import gsap from "gsap";

export const GsapRemotionScene = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const tlRef = useRef<gsap.core.Timeline | null>(null);

  useEffect(() => {
    tlRef.current = gsap.timeline({ paused: true });
    tlRef.current
      .to(".box", { x: 300, duration: 1, ease: "power2.out" })
      .to(".text", { opacity: 1, duration: 0.5 });
  }, []);

  useEffect(() => {
    if (tlRef.current) {
      tlRef.current.seek(frame / fps);
    }
  }, [frame, fps]);

  return <div className="box">GSAP Content</div>;
};
```
