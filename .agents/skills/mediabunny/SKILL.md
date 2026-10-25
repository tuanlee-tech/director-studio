---
name: mediabunny
description: >-
  Kỹ năng WebCodecs & Fast Video Encoding với Mediabunny: Trích xuất metadata video,
  encode video thần tốc ngay trong browser & Node.js, tối ưu hóa pipeline preview phân cảnh thời gian thực.
---

# ⚡ Mediabunny — Encode Video Siêu Tốc Trong Trình Duyệt Bằng WebCodecs

Mediabunny đại diện cho kỷ nguyên encode video hiện đại: Tận dụng phần cứng GPU thông qua chuẩn WebCodecs API của trình duyệt hiện đại để đọc, xử lý và xuất video MP4 với tốc độ gấp nhiều lần các phương pháp truyền thống.

## 🎯 Ứng Dụng Trong Quy Trình Sản Xuất Video
- **Fast Clip Preview**: Xem trước các phân đoạn hoạt ảnh phức tạp (như TreeGrowth hay 3D Coins) ngay lập tức mà không cần chờ render toàn bộ video 5-10 phút.
- **Trích Xuất Metadata & Keyframes Cực Nhanh**: Đọc chính xác FPS, độ dài microsecond, và cấu trúc GOP của video B-roll mà không làm treo UI trình duyệt.
- **Tối Ưu Pipeline Render Cục Bộ**: Hỗ trợ xuất các đoạn video ngắn (Shorts, Reels 1080x1920) với độ trễ thấp nhất.

## ⚡ Các Kỹ Thuật Tối Ưu WebCodecs Pipeline
1. **VideoFrame Lifecycle**: Luôn gọi `frame.close()` sau khi xử lý xong mỗi frame trong canvas để tránh rò rỉ bộ nhớ GPU (VRAM leak).
2. **Hardware Acceleration**: Ưu tiên cấu hình encoder `avc1.640028` (H.264 High Profile) với hardware acceleration `prefer-hardware`.
3. **Audio-Video Multiplexing**: Đảm bảo timestamp âm thanh và hình ảnh khớp tuyệt đối (Monotonic Timestamps) để tránh hiện tượng lệch tiếng (audio drift).
