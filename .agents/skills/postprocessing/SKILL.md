---
name: postprocessing
description: >-
  Kỹ năng hiệu ứng hậu kỳ đồ họa (Postprocessing): Hiệu ứng phát sáng Neon Bloom,
  Depth of Field, Chromatic Aberration, Vignette tạo cảm giác điện ảnh đẳng cấp cho video.
---

# 🎆 Postprocessing — Hiệu Ứng Hậu Kỳ Điện Ảnh Cao Cấp

Postprocessing bổ sung các bộ lọc thị giác (Shaders) lên khung hình hoàn chỉnh, biến một hoạt ảnh thông thường thành một thước phim điện ảnh có chiều sâu và cảm xúc thị giác mạnh mẽ.

## 🎯 Ứng Dụng Trong Video Tài Chính
- **Neon Bloom (Phát sáng rực rỡ)**: Làm con số đỏ nguy hiểm `35%` hoặc các nhánh cây nợ rực sáng như tia laser trong bóng tối.
- **Chromatic Aberration (Quang sai màu)**: Tạo hiệu ứng giật rung lỗi kỹ thuật số (Glitch / Warning) khi có báo động nợ xấu.
- **Vignette (Tối 4 góc)**: Tập trung ánh nhìn của khán giả vào trung tâm khung hình nơi con số tài chính đang thay đổi.
- **Depth of Field (Xóa phông)**: Làm mờ hậu cảnh để làm nổi bật chiếc thẻ tín dụng hoặc con số ở tiền cảnh.

## ⚡ Các Shaders Tiêu Chuẩn

```tsx
import { Bloom, ChromaticAberration, Vignette } from "@react-three/postprocessing";
import { Vector2 } from "three";

export const CinematicEffects = ({ isAlert = false }: { isAlert?: boolean }) => (
  <>
    {/* Ánh sáng neon */}
    <Bloom
      intensity={1.2}
      luminanceThreshold={0.4}
      luminanceSmoothing={0.9}
    />

    {/* Tối góc điện ảnh */}
    <Vignette eskil={false} offset={0.2} darkness={0.8} />

    {/* Quang sai cảnh báo khi báo động */}
    {isAlert && (
      <ChromaticAberration
        offset={new Vector2(0.005, 0.005)}
        radialModulation={false}
        modulationOffset={0}
      />
    )}
  </>
);
```
