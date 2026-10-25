---
name: react-three-fiber
description: >-
  Kỹ năng React Three Fiber (R3F) & @remotion/three: Khai báo 3D Canvas trực tiếp trong React,
  ThreeCanvas component, ánh sáng, camera và đồng bộ rendering từng frame MP4 hoàn hảo.
---

# 🧊 React Three Fiber (R3F) & @remotion/three

React Three Fiber mang sức mạnh của Three.js vào cấu trúc declarative của React. Khi kết hợp với `@remotion/three`, toàn bộ cảnh 3D được đồng bộ hóa với pipeline dựng frame của Remotion.

## 🎯 Ứng Dụng Trong Remotion
- Tích hợp cảnh 3D trực tiếp vào luồng `<Sequence>` của video.
- Điều khiển camera 3D di chuyển lướt qua các mốc thời gian.
- Tạo khối hộp lập phương tài chính xoay 3D với nội dung trên từng mặt.

## ⚡ Mẫu Tích Hợp ThreeCanvas Chuẩn

```tsx
import { ThreeCanvas } from "@remotion/three";
import { useCurrentFrame, useVideoConfig } from "remotion";
import { useRef } from "react";
import * as THREE from "three";

const SpinningCoin = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const meshRef = useRef<THREE.Mesh>(null);

  const rotation = (frame / fps) * Math.PI * 0.8;

  return (
    <mesh ref={meshRef} rotation={[0.3, rotation, 0]}>
      <cylinderGeometry args={[2, 2, 0.3, 32]} />
      <meshStandardMaterial
        color="#F59E0B"
        metalness={0.85}
        roughness={0.15}
      />
    </mesh>
  );
};

export const Three3DScene = () => {
  return (
    <ThreeCanvas width={1920} height={1080}>
      <ambientLight intensity={0.6} />
      <directionalLight position={[5, 10, 7]} intensity={1.2} />
      <SpinningCoin />
    </ThreeCanvas>
  );
};
```

## ⚠️ Lưu Ý Tương Thích
- Sử dụng `@react-three/fiber` phiên bản tương thích với React 18 (`^8.17.x` hoặc `^8.18.x`).
- Tránh gọi `useFrame()` của R3F trong Remotion; thay vào đó, luôn đọc trực tiếp `useCurrentFrame()` của Remotion để đảm bảo đồng bộ frame chính xác khi render xuất file MP4.
