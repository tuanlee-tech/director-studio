---
name: howler
description: >-
  Kỹ năng quản lý âm thanh & Sound FX với Howler.js: Phát nhạc nền BGM, frame-accurate sound effects (SFX),
  tiếng keng nhảy số, tiếng còi hú cảnh báo, audio ducking khi có giọng đọc narration.
---

# 🔊 Howler.js — Quản Lý Nhạc Nền (BGM) & Hiệu Ứng Âm Thanh (Sound FX)

Howler.js là thư viện âm thanh tiêu chuẩn cho web và ứng dụng, mang lại khả năng kiểm soát âm lượng, phát SFX chính xác từng frame, và tự động xử lý audio sprite.

## 🎯 Ứng Dụng Trong Video Remotion
- **Kích Hoạt SFX Đúng Frame**:
  - Tiếng "Keng" kim loại khi con số 40.000.000 VNĐ nhảy xong.
  - Tiếng "Whoosh" khi thẻ cảnh báo trượt vào từ cạnh màn hình.
  - Tiếng "Buzzer / Siren" dồn dập khi hiển thị cảnh báo lãi suất 35%.
  - Tiếng "Cash Register / Ting Ting" khi tất toán nợ thành công.
- **Audio Ducking (Tự động hạ nhạc nền)**:
  - Tự động hạ âm lượng BGM xuống 15% khi người thuyết minh (narration) đang nói.
  - Tăng nhẹ BGM lên 30% trong các khoảng lặng giữa 2 câu thoại để tạo nhịp điệu lôi cuốn.

## ⚡ Mẫu Điều Khiển Âm Lượng & SFX Trong Remotion
```tsx
import { Audio, interpolate } from "remotion";

export const BackgroundMusicTrack = ({
  src,
  narrationActive = true,
}: {
  src: string;
  narrationActive?: boolean;
}) => {
  // Volume ducking tự động
  const targetVolume = narrationActive ? 0.12 : 0.28;

  return (
    <Audio
      src={src}
      volume={(f) => interpolate(f, [0, 30], [0, targetVolume], { extrapolateRight: "clamp" })}
      loop
    />
  );
};
```
