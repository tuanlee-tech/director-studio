---
name: drei
description: >-
  Kỹ năng sử dụng @react-three/drei: Bộ helper dựng sẵn cho R3F, Float (bập bênh vật thể 3D),
  Text3D (chữ 3D nổi bật), Sparkles (đốm sáng vàng tài chính), Environment và ContactShadows.
---

# ✨ Drei — Bộ Trợ Thủ Cao Cấp Cho React Three Fiber

Drei cung cấp hàng trăm component helper sẵn dùng giúp tiết kiệm thời gian khi dựng không gian 3D chất lượng cao trong video.

## 🎯 Các Helper Thường Dùng Cho Video Tài Chính

1. **`<Float>`**:
   - Tự động tạo chuyển động bập bênh bồng bềnh tự nhiên cho đồng tiền vàng hoặc thẻ tín dụng.
   - Tham số: `speed={2}`, `rotationIntensity={1}`, `floatIntensity={1.5}`.
2. **`<Text3D>`**:
   - Dựng các con số tài chính 3D khổng lồ nổi bật: `40.000.000 VNĐ` hoặc `35% LÃI SUẤT`.
   - Tạo khối chữ nổi với bevel đẹp mắt.
3. **`<Sparkles>`**:
   - Hàng chục đốm sáng vàng lấp lánh xung quanh hòm tiền hoặc biểu tượng tích sản.
   - Tham số: `count={60}`, `scale={6}`, `size={4}`, `speed={0.4}`, `color="#FDE047"`.
4. **`<ContactShadows>`**:
   - Tạo bóng đổ tiếp xúc mềm mại trên mặt sàn phía dưới vật thể, tăng độ chân thực không gian.

## ⚡ Ví Dụ Thẻ Tín Dụng 3D Bập Bênh
```tsx
import { Float, Sparkles, ContactShadows } from "@react-three/drei";

export const FloatingCard3D = () => (
  <group>
    <Float speed={2.5} rotationIntensity={0.6} floatIntensity={1.2}>
      <mesh>
        <boxGeometry args={[3.4, 2.1, 0.08]} />
        <meshStandardMaterial color="#1E293B" metalness={0.9} roughness={0.1} />
      </mesh>
    </Float>
    <Sparkles count={40} scale={5} size={3} color="#F59E0B" />
    <ContactShadows position={[0, -2, 0]} opacity={0.6} scale={10} blur={2.5} />
  </group>
);
```
