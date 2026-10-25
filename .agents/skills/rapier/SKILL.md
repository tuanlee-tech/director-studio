---
name: rapier
description: >-
  Kỹ năng mô phỏng vật lý 3D với Rapier (@react-three/rapier): Rơi tự do, trọng lực,
  tiền xu vàng rơi va chạm chất đống, khối nợ đè bẹp dòng tiền, tương tác va đập thời gian thực.
---

# 💥 Rapier — Mô Phỏng Vật Lý 3D Chân Thực Cho Video

Rapier (chạy trên WebAssembly Rust) là động cơ vật lý 3D tốc độ cao, hỗ trợ mô phỏng trọng lực (Gravity), va chạm đa vật thể (RigidBody collisions), và xếp chồng vật lý.

## 🎯 Ứng Dụng Trong Video Tài Chính
- **Mưa tiền xu chất đống (Coin Stacking)**: Khi nói về tích sản đều đặn mỗi tháng, hàng chục đồng tiền vàng rơi từ trên xuống, va chạm nảy tưng bừng và xếp thành tháp tài sản.
- **Khối nợ đè bẹp đòn bẩy**: Khối hộp đen khổng lồ `LÃI SUẤT 35%` rơi xuống đè bẹp cán cân chi tiêu.
- **Hiệu ứng vỡ vụn (Shatter)**: Chiếc thẻ tín dụng bị vỡ tan thành từng mảnh vụn văng ra xung quanh khi cắt thẻ.

## ⚡ Cấu Trúc Khởi Tạo Vật Lý Trong R3F
```tsx
import { Physics, RigidBody } from "@react-three/rapier";

export const FallingCoinsPhysics = () => {
  return (
    <Physics gravity={[0, -9.81, 0]}>
      {/* Sàn đỡ cố định */}
      <RigidBody type="fixed">
        <mesh position={[0, -3, 0]}>
          <boxGeometry args={[10, 0.5, 10]} />
          <meshStandardMaterial color="#0F172A" />
        </mesh>
      </RigidBody>

      {/* Các đồng xu rơi tự do và va chạm */}
      {[...Array(20)].map((_, i) => (
        <RigidBody
          key={i}
          position={[(Math.random() - 0.5) * 3, 5 + i * 0.8, (Math.random() - 0.5) * 3]}
          restitution={0.6} // Độ nảy
          friction={0.8}    // Độ ma sát
        >
          <mesh>
            <cylinderGeometry args={[0.6, 0.6, 0.1, 16]} />
            <meshStandardMaterial color="#F59E0B" metalness={0.9} roughness={0.1} />
          </mesh>
        </RigidBody>
      ))}
    </Physics>
  );
};
```
