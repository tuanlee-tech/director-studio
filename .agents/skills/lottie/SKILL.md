---
name: lottie
description: >-
  Kỹ năng hoạt ảnh Lottie trong Remotion qua @remotion/lottie: Phát animation xuất từ After Effects,
  pháo hoa ăn mừng, dấu mộc ĐÃ THANH TOÁN dập xuống, chuông báo động rung lắc và điều khiển frame chính xác.
---

# 📦 Lottie — Hoạt Ảnh After Effects Vector Với @remotion/lottie

Lottie cho phép nạp các file hoạt ảnh vector JSON xuất từ Adobe After Effects (Bodymovin) trực tiếp vào video Remotion với độ sắc nét tuyệt đối và đồng bộ từng frame.

## 🎯 Ứng Dụng Trong Video Tài Chính
- **Dấu mộc đỏ dập xuống**: Con dấu `ĐÃ THANH TOÁN 100%` hoặc `HỦY LIÊN KẾT` đập mạnh vào hợp đồng tín dụng.
- **Pháo hoa chúc mừng (Confetti)**: Bắn pháo hoa rực rỡ khi hoàn thành bước 4: Trả hết toàn bộ dư nợ.
- **Chuông cảnh báo rung lắc**: Rung lắc dữ dội khi chạm đến ngày thứ 45 chu kỳ miễn lãi.

## ⚡ Mẫu Code Sử Dụng @remotion/lottie Chuẩn Xác

```tsx
import { Lottie } from "@remotion/lottie";
import { useCurrentFrame } from "remotion";
import alertAnimationData from "./assets/alert-bell.json";

export const LottieAlertScene = () => {
  const frame = useCurrentFrame();

  return (
    <div style={{ display: "flex", justifyContent: "center", alignItems: "center", width: "100%", height: "100%" }}>
      <div style={{ width: 400, height: 400 }}>
        <Lottie
          animationData={alertAnimationData}
          // Lottie tự động đồng bộ theo frame hiện tại của Remotion
        />
      </div>
    </div>
  );
};
```

## ⚠️ Lưu Ý Quan Trọng
- **Tránh Fetch URL Ngoài**: Luôn lưu JSON asset trong repo hoặc bundle nội bộ, tránh gọi CDN bên ngoài khi render headless vì sẽ gây lỗi timeout.
- **Tối Ưu Dung Lượng**: File Lottie JSON nên dưới 500KB để đảm bảo tốc độ render MP4 nhanh nhất.
