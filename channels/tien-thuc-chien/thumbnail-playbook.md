# CẨM NANG TOÀN TẬP: KHÓA PHONG CÁCH NHÂN VẬT & TẠO THUMBNAIL YOUTUBE CHUẨN VOX STYLE
*(OFFICIAL CHARACTER STYLE LOCK & YOUTUBE THUMBNAIL PRODUCTION PLAYBOOK)*

---

## 📌 PHẦN 1: STYLE LOCK NHÂN VẬT ĐẠI DIỆN KÊNH

### 1. Thông Tin Nhận Diện
- **Hình tượng**: Chàng trai Việt Nam 26–28 tuổi, gương mặt sáng sủa, trí thức, gần gũi, đáng tin cậy.
- **Đặc điểm cố định**:
  - Tóc đen ngắn vuốt textured nhẹ, có lọn mái bay tự nhiên.
  - Kính mắt gọng vuông đen mỏng hiện đại.
  - Áo sơ mi trắng cổ bẻ, đeo thẻ nhân viên công sở (hoặc áo nỉ xám than khi ở nhà).
- **Chất liệu mỹ thuật**: Semi-realistic Digital Illustration, Modern Graphic Novel style, nét mực đen tinh xảo (`fine black line art`), đổ bóng cel-shading mềm mại kết hợp ánh sáng điện ảnh ấm áp.
- **Tệp mỏ neo gốc**: [`channels/tien-thuc-chien/characters/master_anchor.png`](file:///c:/Users/tuanlee/Downloads/audio/channels/tien-thuc-chien/characters/master_anchor.png) (Độ phân giải siêu nét: `2752 x 1536`).

### 2. Prompt Gốc Tạo Master Anchor (Google Flow)
```text
Waist-up character portrait of a 27-year-old Vietnamese young professional man, modern handsome intellectual appearance. Short textured stylish black hair, wearing modern thin rectangular black-rimmed eyeglasses. Friendly confident and approachable smile, looking slightly off-camera. Wearing a crisp clean white collared button-down shirt with a dark lanyard ID badge around his neck. Semi-realistic digital illustration, modern graphic novel art style, clean fine black line art, soft smooth cel-shading, warm natural skin tones. Soft natural studio daylight, plain neutral off-white background. High resolution, 8k, masterpiece character concept art.
```

### 3. Negative Prompt Bắt Buộc
```text
Photorealism, 3D render, CGI, Unreal Engine, flat 2D cartoon, Vyond style, chibi, exaggerated caricature, messy sketch, watercolor, deformed hands, extra fingers, distorted eyes, blurry, low resolution, noisy, watermark, text.
```

---

## 📌 PHẦN 2: QUY TRÌNH WARM-UP ĐỒNG NHẤT 5 CỬA SỔ GOOGLE FLOW

Khi tạo Project ID mới trên Google Flow để sinh hình ảnh cho video:

1. **Thao tác thủ công mồi (1 lần duy nhất đầu dự án)**:
   - Mở 5 profile Chrome Google Flow (Cổng `9223`, `9224`, `9225`, `9226`, `9227`).
   - Tạo Project mới trên cả 5 cửa sổ.
   - **Kéo thả tệp `master_anchor.png` vào ô đầu tiên của cả 5 cửa sổ** làm ảnh tham chiếu (Style & Character Anchor).
2. **Cơ chế gọi prompt tự động (`flow-dispatcher`)**:
   - Khi chạy kịch bản tự động chia batch prompt cho 5 tài khoản, mọi prompt cảnh có sự xuất hiện của nhân vật đều được mở đầu bằng câu thần chú:
     > *"Using the young Vietnamese man with glasses from the reference image, [hành động cụ thể của cảnh]..."*
   - Cả 5 tài khoản sẽ tự động đồng bộ 100% gương mặt, kiểu tóc và trang phục của nhân vật cho mọi cảnh từ đầu đến cuối video.

---

## 📌 PHẦN 3: KHO 10 STICKER BIỂU CẢM VOX STYLE ĐÃ TÁCH NỀN

Toàn bộ 10 file PNG trong suốt đã được lưu trữ sẵn sàng tại:
📂 [`channels/tien-thuc-chien/characters/`](file:///c:/Users/tuanlee/Downloads/audio/channels/tien-thuc-chien/characters/)

| File Sticker | Kích Thước | Kênh Màu | Biểu Cảm & Hành Động |
| :--- | :--- | :--- | :--- |
| `cutting.png` | `528 x 677` | RGBA | Cầm kéo cắt thẻ tín dụng (Pose chính của video Thoát bẫy nợ) |
| `confident.png` | `506 x 676` | RGBA | Khoanh tay mỉm cười tự tin, làm chủ tài chính |
| `shock.png` | `554 x 668` | RGBA | Mắt mở to kinh ngạc nhìn số dư nợ / sao kê |
| `stress.png` | `586 x 678` | RGBA | Một tay ôm trán áp lực vì lãi suất cao |
| `thinking.png` | `507 x 699` | RGBA | Chống cằm suy nghĩ, tính toán chi phí cơ hội |
| `warning.png` | `599 x 672` | RGBA | Giơ tay cảnh báo cạm bẫy trả tối thiểu |
| `pointing.png` | `539 x 679` | RGBA | Chỉ tay sang bên phải vào biểu đồ hoặc số liệu |
| `holding_card.png` | `542 x 676` | RGBA | Cầm thẻ ngân hàng phân tích các loại phí |
| `celebrating.png` | `585 x 673` | RGBA | Giơ 2 tay ăn mừng mốc Dư nợ = 0 đồng |
| `stop.png` | `506 x 661` | RGBA | Giơ 2 tay ra hiệu dừng quẹt thẻ |

---

## 📌 PHẦN 4: HỆ THỐNG KẾT XUẤT THUMBNAIL REMOTION TỰ ĐỘNG

### 1. Bố Cục Chuẩn Vàng (Golden Layout)
- **Bên Trái (44% Width)**: Nhân vật sticker với góc đứng 3/4 hướng mắt vào trong, bọc viền trắng nổi khối Vox Style (`drop-shadow multi-layer outline`) và đổ bóng điện ảnh sâu.
- **Bên Phải (56% Width)**: 
  - Huy hiệu kênh: `🔥 TIỀN THỰC CHIẾN • QUY TRÌNH 4 BƯỚC`
  - Tiêu đề 3D siêu đậm: `THOÁT BẪY NỢ` (Vàng chanh #FFE600) + `THẺ TÍN DỤNG` (Trắng sáng #FFFFFF).
  - Khối so sánh mốc lộ trình: `DƯ NỢ 40 TRIỆU` (Đỏ) ➔ `SAU 10 THÁNG: 0 ĐỒNG!` (Xanh).
  - Dòng bảo chứng: `✓ Áp dụng cho thu nhập 10 - 12 triệu/tháng`.
- **Góc dưới bên phải**: Chừa trống an toàn, hoàn toàn không bị nhãn thời lượng video của YouTube (`06:49`) che lấp.

### 2. Lệnh Xuất Bản Thumbnail CLI Nhanh
Sử dụng script [`tools/render_thumbnail.py`](file:///c:/Users/tuanlee/Downloads/audio/tools/render_thumbnail.py):

```bash
# 1. Xuất Thumbnail mặc định (Pose cắt thẻ, bên trái, Full HD 1080p):
python tools/render_thumbnail.py --pose cutting

# 2. Xuất Thumbnail biểu cảm Tự Tin:
python tools/render_thumbnail.py --pose confident

# 3. Xuất Thumbnail biểu cảm Sốc dư nợ:
python tools/render_thumbnail.py --pose shock

# 4. Xuất Thumbnail tùy chỉnh toàn bộ tiêu đề & số tiền cho video mới:
python tools/render_thumbnail.py --pose thinking \
  --title1 "QUY TẮC 33%" \
  --title2 "QUẢN LÝ TIỀN LƯƠNG" \
  --debt-start "LƯƠNG 10TR" \
  --debt-target "DƯ 3.5 TRIỆU" \
  --time-frame "MỖI THÁNG" \
  --badge "TIỀN THỰC CHIẾN • TÍCH SẢN"
```

---

## 📌 PHẦN 5: CHECKLIST KIỂM TRA TRƯỚC KHI XUẤT BẢN YOUTUBE

- [ ] **Độ sắc nét**: Kích thước file đạt chuẩn `1920 x 1080 px` (Full HD) hoặc tối thiểu `1280 x 720 px`.
- [ ] **Kiểm tra vùng an toàn (Safe Zone)**: Đảm bảo góc dưới cùng bên phải (chiếm 20% chiều rộng x 15% chiều cao) không chứa bất kỳ chữ hay chi tiết quan trọng nào.
- [ ] **Độ tương phản trên màn hình nhỏ**: Thu nhỏ màn hình xuống kích thước 150px (mô phỏng xem trên điện thoại di động) xem dòng chữ `THOÁT BẪY NỢ` và mốc `0 ĐỒNG!` có đọc rõ mồn một trong 0.5 giây đầu tiên không.
- [ ] **Đồng nhất nhân vật**: Nhân vật trên thumbnail có trùng khớp hoàn toàn với nhân vật trong video không (cùng chàng trai đeo kính, sơ mi trắng).
