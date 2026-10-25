---
name: threejs
description: >-
  Kỹ năng đồ họa 3D Three.js: Tạo cảnh WebGL chiều sâu, meshes lập phương, hạt bụi lơ lửng (particle systems),
  vật liệu kim loại (metallic) & phản chiếu ánh sáng cho các biểu tượng tài chính sang trọng.
---

# 🌐 Three.js — Đồ Họa 3D WebGL Chiều Sâu Cho Video

Three.js cho phép đưa không gian 3 chiều vào video Remotion: Ánh sáng chân thực, bóng đổ động, vật liệu phản xạ và các trường hạt bụi phát sáng tạo cảm giác điện ảnh đẳng cấp.

## 🎯 Ứng Dụng Trong Video Tài Chính
- **Đồng tiền vàng 3D xoay tròn**: Đồng xu Bitcoin / VNĐ vàng óng phản chiếu ánh sáng môi trường.
- **Thẻ tín dụng 3D bập bênh trong không gian**: Thẻ đen Black Card xoay góc nghiêng sang trọng.
- **Trường hạt bụi lơ lửng (Ambient Dust Particles)**: Hàng nghìn hạt bụi vàng li ti bay lơ lửng tạo chiều sâu cho khung hình.

## ⚡ Các Kỹ Thuật Three.js Tối Ưu Cho Remotion
1. **Khởi Tạo Cảnh Nhẹ Nhàng**:
   - Sử dụng `BufferGeometry` tối ưu bộ nhớ.
   - Giới hạn số lượng polygon (`geometry segments <= 32`).
2. **Ánh Sáng & Vật Liệu**:
   - Dùng `MeshStandardMaterial` với `metalness: 0.8`, `roughness: 0.2` để tạo bề mặt kim loại vàng/bạc bóng loáng.
   - Kết hợp `DirectionalLight` và `AmbientLight` nhẹ nhàng.
3. **Đồng Bộ Hoạt Ảnh Theo Frame**:
   ```ts
   mesh.rotation.y = (frame / fps) * Math.PI * 0.5;
   mesh.position.y = Math.sin(frame / 15) * 0.2;
   ```
