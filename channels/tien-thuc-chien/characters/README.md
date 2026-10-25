# HƯỚNG DẪN BỘ NHÂN VẬT NHẬN DIỆN KÊNH TIỀN THỰC CHIẾN
*(Master Character Anchor & 9 Vox-Style Expressions)*

## 1. File Nhân vật Gốc (Master Anchor)
- **Tên file**: `master_anchor.png`
- **Mục đích**: Làm hình ảnh tham chiếu (Style & Character Reference) đính kèm vào ô đầu tiên của 5 cửa sổ Google Flow để warm-up đồng nhất nhân vật.
- **Prompt tạo Master Anchor (Google Flow)**:
```text
Character concept art, 2D flat vector cartoon, Vyond animation style, thick black outlines, solid vibrant colors. A confident 28-year-old Vietnamese man, modern haircut, friendly approachable face, wearing a dark grey polo shirt. Standing in a neutral three-quarter pose against a pure solid white background. Clean composition, highly recognizable character design. No 3D render, no CGI, no photorealism.
```

---

## 2. Prompt Tạo Lưới 9 Biểu Cảm (3x3 Expression Grid)
Dùng sau khi đã đính kèm `master_anchor.png` làm ảnh tham chiếu trên Google Flow:
```text
Using the exact character from the reference image, generate a 3x3 character expression sheet showing 9 different financial reactions and poses:
1. SHOCK: shocked wide eyes looking at bank app balance
2. STRESS: holding head with hands feeling financial pressure
3. THINKING: chin resting on hand analyzing debt numbers
4. WARNING: hand raised in warning against credit card traps
5. CUTTING: holding large red scissors cutting a credit card
6. POINTING: pointing confidently to the right side
7. HOLDING_CARD: holding a credit card and money cash
8. CONFIDENT: arms crossed smiling confidently
9. CELEBRATING: two arms raised celebrating zero debt freedom
Solid white background, 2D flat vector cartoon, Vyond style, thick black outlines, clean separate panels.
```

---

## 3. Quy ước đặt tên 9 file PNG trong suốt (Vox Style Cutouts)
Sau khi tách nền, lưu các file vào thư mục này:
1. `shock.png` — Sốc khi thấy dư nợ / lãi suất
2. `stress.png` — Áp lực, lo lắng vì nợ
3. `thinking.png` — Chống cằm suy nghĩ, tính toán chi phí
4. `warning.png` — Giơ tay cảnh báo bẫy tài chính
5. `cutting.png` — Cầm kéo cắt thẻ tín dụng
6. `pointing.png` — Chỉ tay vào biểu đồ hoặc tiêu đề
7. `holding_card.png` — Cầm thẻ / tiền
8. `confident.png` — Tự tin, mỉm cười khoanh tay
9. `celebrating.png` — Ăn mừng chạm mốc Dư nợ = 0 đồng
