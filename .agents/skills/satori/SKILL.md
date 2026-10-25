---
name: satori
description: >-
  Kỹ năng thiết kế đồ họa với Satori: Biến HTML/JSX thành SVG động, tự động tính toán
  bố cục Flexbox, dynamic typography, chống tràn text, không đè lấn tiêu đề trên khung hình 16:9.
---

# 🎨 Satori — Biến JSX & HTML Thành Vector SVG Động Sắc Nét

Satori (từ Vercel) cho phép chuyển đổi các thẻ JSX và CSS Flexbox thành đồ họa vector SVG chuẩn xác. Đây là giải pháp hoàn hảo để sinh các thẻ thông tin (Infographic Cards), bảng so sánh lãi suất, và biểu đồ tài chính không bao giờ bị vỡ hạt hay đè lấn layout.

## 🎯 Ứng Dụng Trong Video Remotion
- **Chống Đè Tiêu Đề (Decoupled Layout)**: Sử dụng mô hình Flexbox chuẩn xác để tính toán chiều cao tự động cho thẻ bài cảnh báo, so sánh số liệu lãi suất `6%` vs `35%`.
- **Đồ Họa Vector Sắc Nét 4K**: SVG sinh từ Satori giữ nguyên độ nét tuyệt đối ở mọi độ phân giải (1080p, 2K, 4K).
- **Hỗ trợ Font Chữ Tiếng Việt**: Tích hợp các bộ font Google Fonts (`Be Vietnam Pro`, `Montserrat`, `Roboto`) đầy đủ dấu thanh tiếng Việt.

## 📐 Nguyên Tắc Thiết Kế Bố Cục Chống Tràn Text
1. **Container Luôn Có Đệm Rộng Rãi**:
   - Header container: `padding: '32px 48px'`, `marginBottom: '36px'`.
   - Content wrapper: `display: 'flex'`, `flexDirection: 'column'`, `gap: '24px'`.
2. **Kích Thước Text Cân Đối**:
   - Headline: `fontSize: 44`, `fontWeight: 800`, `lineHeight: 1.25`.
   - Sub-headline / Metric: `fontSize: 28`, `fontWeight: 600`.
   - Value Accent: `fontSize: 54`, `fontWeight: 900`, `color: '#EF4444'`.
3. **Mô Hình Box-Sizing & Flex-Shrink**:
   - Mọi phần tử con phải có `flexShrink: 0` khi cần cố định kích thước.
   - Text dài phải có `wordBreak: 'break-word'` hoặc tự động xuống dòng với `display: 'flex'`.

## 💻 Mẫu Thẻ Infographic Tài Chính Chuẩn Satori / JSX
```tsx
export const SatoriStyleCard = ({ title, value, subtitle, tag }: {
  title: string;
  value: string;
  subtitle: string;
  tag: string;
}) => (
  <div
    style={{
      display: 'flex',
      flexDirection: 'column',
      width: '850px',
      backgroundColor: 'rgba(15, 23, 42, 0.88)',
      backdropFilter: 'blur(20px)',
      borderRadius: '24px',
      border: '2px solid rgba(239, 68, 68, 0.4)',
      padding: '40px 48px',
      boxShadow: '0 25px 60px -15px rgba(0, 0, 0, 0.8)',
    }}
  >
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
      <span style={{ fontSize: '18px', fontWeight: 700, color: '#EF4444', textTransform: 'uppercase', letterSpacing: '2px' }}>
        {tag}
      </span>
      <div style={{ width: '12px', height: '12px', borderRadius: '50%', backgroundColor: '#EF4444', boxShadow: '0 0 12px #EF4444' }} />
    </div>
    
    <div style={{ fontSize: '36px', fontWeight: 800, color: '#FFFFFF', marginBottom: '16px', lineHeight: 1.25 }}>
      {title}
    </div>
    
    <div style={{ fontSize: '64px', fontWeight: 900, color: '#F59E0B', marginBottom: '16px', letterSpacing: '-1px' }}>
      {value}
    </div>
    
    <div style={{ fontSize: '20px', color: '#94A3B8', lineHeight: 1.4 }}>
      {subtitle}
    </div>
  </div>
);
```
