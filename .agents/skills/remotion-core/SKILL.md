---
name: remotion-core
description: >-
  Kỹ năng cốt lõi Remotion Engine: Biến React code thành từng frame MP4 chuẩn xác,
  Composition, Sequence, Series, Loop, AbsoluteFill, useCurrentFrame, interpolate, spring, OffthreadVideo.
---

# 🎥 Remotion Core — Động Cơ Dựng Video Bằng React & TypeScript

Remotion Core là nền tảng biến mã nguồn React thành từng khung hình video độ phân giải cao (FullHD 1080p, 4K), xuất ra định dạng MP4 hoặc ProRes chuẩn công nghiệp.

## 🧱 Cấu Trúc Khối Thành Phần Video Chuẩn

```tsx
<Composition
  id="MainVideo"
  component={VideoComposition}
  durationInFrames={totalFrames}
  fps={30}
  width={1920}
  height={1080}
  defaultProps={{ ... }}
/>
```

## 🏗️ 5 Nguyên Tắc Bố Cục Video Bất Biến

1. **Phân Tách Sequence & Series**:
   - Dùng `<Sequence from={startFrame} durationInFrames={sceneDuration}>` để cô lập từng cảnh thị giác.
   - Tránh đặt sequence chồng chéo gây xung đột âm thanh hoặc đè hình.
2. **Layering Chuẩn Mực**:
   - **Layer 1 (Đáy)**: Background Video / Ken Burns Image / 3D Canvas (`zIndex: 0`).
   - **Layer 2 (Giữa)**: Motion Graphics Overlay / Infographic Cards / TreeGrowth (`zIndex: 10`).
   - **Layer 3 (Cận đỉnh)**: Subtitle Karaoke Trong Suốt (`zIndex: 20`).
   - **Layer 4 (Đỉnh)**: Channel Watermark / Viền Cinematic (`zIndex: 30`).
   - **Audio Track**: Nằm độc lập qua thẻ `<Audio />` với volume ducking.
3. **Nội Suy Chuyển Động An Toàn**:
   - Luôn đặt `extrapolateLeft: "clamp"` và `extrapolateRight: "clamp"` để tránh giá trị bay ra ngoài biên vô tận khi hết thời lượng cảnh.
4. **Xử Lý Video Nền**:
   - Dùng `<OffthreadVideo>` cho render headless CLI để tối đa hóa tốc độ decode.
   - Nạp media qua URL API Flask cục bộ (`http://127.0.0.1:3000/api/media/...`) hoặc `staticFile()`.
5. **Không Rò Rỉ Biến Toàn Cục**:
   - Mọi trạng thái hoạt ảnh phải phụ thuộc thuần túy (pure function) vào `useCurrentFrame()`.
