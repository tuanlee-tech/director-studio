---
name: remotion-skills
description: >-
  Official Remotion AI skills from remotion-dev/skills: Best practices for frame-based React video,
  markup structure, compositions, sequences, series, transitions, captions, audio, and studio preview.
---

# 🎬 Remotion Skills (Official remotion-dev/skills)

Bộ kỹ năng chính thức từ đội ngũ phát triển Remotion hướng dẫn AI lập trình video React chuẩn xác, tối ưu hiệu năng và không lỗi cú pháp.

## 📌 Các Module Chính

1. **[Best Practices](./remotion-best-practices/SKILL.md)**: Quy tắc chung về cấu trúc project, render và workflow.
2. **[Markup Guidelines](./remotion-markup/REFERENCE.md)**: Cách viết thẻ `<Sequence>`, `<AbsoluteFill>`, `<Loop>`, `<Series>`, `<Freeze>`.
3. **[Captions & Subtitles](./remotion-captions/REFERENCE.md)**: Xử lý phụ đề từng từ, karaoke timing, font chữ và text animation.
4. **[Multimedia & Audio](./remotion-multimedia/REFERENCE.md)**: Xử lý video, audio narration, BGM, volume ramping và fade.
5. **[Studio & Interactive Preview](./remotion-studio/REFERENCE.md)**: Sử dụng Remotion Studio (`npx remotion preview`) để review trực quan trước khi render.
6. **[Render & CLI](./remotion-render/REFERENCE.md)**: Cấu hình `remotion render`, still render, GL backend, port và codec.

## ⚡ Quy Tắc Vàng Khi Viết Remotion Code

- **Luôn dựa trên frame**: Mọi hoạt ảnh là hàm số của `useCurrentFrame()`. Không bao giờ dùng `setTimeout`, `setInterval` hay `requestAnimationFrame`.
- **Nội suy chuyển động**: Dùng `interpolate(frame, [start, end], [fromVal, toVal], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' })`.
- **Vật lý Spring**: Dùng `spring({ frame, fps, config: { damping: 14, mass: 0.8, stiffness: 120 } })`.
- **Không bao giờ chặn rendering**: Tránh async trong render; nạp tài nguyên tĩnh qua `staticFile()` hoặc `preloadAudio()` / `preloadVideo()`.
