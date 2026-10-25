---
name: rive
description: >-
  Kỹ năng tích hợp Rive Animation: Hoạt ảnh 2D có State Machine tương tác, nhân vật biểu cảm theo tình huống tài chính,
  chuyển trạng thái cảm xúc (lo lắng -> tự tin) và đồng bộ frame Remotion.
---

# 🎭 Rive — Hoạt Ảnh 2D Vector State Machine Chuyên Nghiệp

Rive cho phép tạo ra các hoạt ảnh vector 2D thời gian thực với hệ thống **State Machine** phức tạp. Trong video tài chính faceless, Rive mang lại các nhân vật đại diện (Avatar) hoặc biểu tượng tương tác thay đổi trạng thái theo ngữ cảnh kịch bản.

## 🎯 Ứng Dụng Trong Video
- **Nhân vật biểu cảm cảm xúc**: Người tiêu dùng hoảng hốt khi nợ tăng vọt -> Vui mừng thở phào khi hoàn thành bước 4 tất toán thẻ.
- **Hộp an toàn / Ổ khóa tài chính**: Ổ khóa đóng chặt khi bảo mật -> Tự động xoay mã và mở bung khi nhập đúng chiến lược 4 bước.
- **Biểu đồ cột có mắt và cảm xúc sống động**: Làm sinh động các con số tài chính khô khan.

## ⚡ Nguyên Tắc Tích Hợp Remotion
1. **Nạp Asset Cục Bộ**: Lưu file `.riv` trong thư mục `public/` hoặc asset của kênh và nạp qua `staticFile()`.
2. **Kích Hoạt State Machine Theo Frame**:
   - Dùng frame Remotion để điều khiển `input` của State Machine:
   ```tsx
   import { useCurrentFrame } from "remotion";
   // Tại frame 30: input "isPanicked" = true
   // Tại frame 90: input "isRelieved" = true
   ```
3. **Fallback Vector Thanh Lịch**: Nếu không có file `.riv`, tự động render SVG Animated Vector tương đương (như `TreeGrowth.tsx` hoặc `InfinityVortex.tsx`) để đảm bảo quá trình render không bị gián đoạn.
