# CHECKPOINT & BACKLOG: DỰ ÁN THOÁT BẪY NỢ THẺ TÍN DỤNG

> **Thời điểm ghi nhận Checkpoint**: 2026-10-26T08:46:00+07:00  
> **Kênh**: `tien-thuc-chien`  
> **Video Target**: `thoat-bay-no-the-tin-dung`  
> **Trạng thái**: Đã thống nhất 100% qua quy trình `/grill-me`, đã hoàn tất đóng dấu che Watermark Gemini 32/32 ảnh tĩnh và căn chỉnh khít 100% overlay AIV.

---

## 📌 1. Tóm Tắt Quyết Định Đã Thống Nhất (/grill-me)

1. **Phân bổ 10 AIV (2 AIV / tài khoản cho 5 tài khoản Google Flow)**:
   - **Account 1** (Port 9223): `S001` (AIV) + `S002` (AIV) *(Đã xong & sạch 100%)*
   - **Account 2** (Port 9224): `S003` (AIV) + `S004` (AIV) *(Đã xong & sạch 100%)*
   - **Account 3** (Port 9225): `S007` (SB $\rightarrow$ AIV) + `S011` (SB $\rightarrow$ AIV) *(Cần sinh mới)*
   - **Account 4** (Port 9226): `S052` (SB $\rightarrow$ AIV) + `S058` (SB $\rightarrow$ AIV) *(Cần sinh mới)*
   - **Account 5** (Port 9227): `S064` (AIV - *Đã xong*) + `S081` (SB $\rightarrow$ AIV - *Cần sinh mới, thay ảnh lỗi tay*)

2. **Quy trình Dispatcher 1-by-1**:
   - Mỗi account chỉ gửi lệnh tạo đúng 1 scene tại một thời điểm.
   - Card/tile hoàn tất $\rightarrow$ Tải media về $\rightarrow$ Chạy QA ngay lập tức.
   - Nếu PASS $\rightarrow$ Gửi tạo scene kế tiếp.
   - Nếu FAIL $\rightarrow$ Thử lại tối đa 1 lần (max 1 retry). Nếu vẫn fail $\rightarrow$ đưa vào `failed_assets_review.json` cho human review và tự động chuyển sang scene tiếp theo.

3. **Storyboard $\rightarrow$ AIV chung 1 Account**:
   - Tài khoản nào tạo Storyboard (ảnh tĩnh tham chiếu) thì dùng chính ảnh đó để sinh video AIV ngay trên tài khoản đó.

4. **Phân khối ảnh tĩnh (IMG) theo Cụm Nhân vật & Tuyến truyện**:
   - Nhóm Nam Host $\rightarrow$ Tập trung tài khoản riêng.
   - Nhóm Người A (Nam) $\rightarrow$ Tập trung tài khoản riêng.
   - Nhóm Người B (Nữ) $\rightarrow$ Tập trung tài khoản riêng.

5. **Đóng dấu thương hiệu `badge_pill.png` che logo Gemini**:
   - **Ảnh tĩnh**: Đã đóng dấu với tọa độ tâm sao `Star Y = h - 95px`, `margin_right = 50 * scale` chống tràn viền khi Ken Burns. Hiệu ứng `KenBurnsImage` tinh chỉnh `scale: [1.0, 1.08]` mượt mà, không bị crop mép viền. Bản gốc bảo toàn tại `assets/raw_backup/`.
   - **Video AIV**: Căn chỉnh overlay `badge_pill.png` tại `bottom: 130, right: 28, width: 410`, che khít 100% ngôi sao watermark cả đỉnh trên lẫn mép dưới (không còn hở bất kỳ pixel nào).

---

## ✅ 2. Những Việc ĐÃ HOÀN TẤT Tại Checkpoint Này

- [x] Tạo công cụ `tools/watermark/stamp_badge_pill.py` hỗ trợ tính toán tọa độ che chuẩn xác.
- [x] Tạo thư mục sao lưu `assets/raw_backup/` bảo vệ 32 file ảnh nguyên bản.
- [x] Đóng dấu thương hiệu `badge_pill.png` cho toàn bộ **32/32 ảnh tĩnh** hiện hữu và đồng bộ sang `studio/remotion/public/assets/`.
- [x] Tinh chỉnh `KenBurnsImage` (scale `[1.0, 1.08]`) đảm bảo không bị cắt viền pill khi zoom-in/pan.
- [x] Tinh chỉnh overlay `badge_pill.png` cho AIV video (`bottom: 130, right: 28, width: 410`) che khít 100% watermark.
- [x] Thiết lập bản kế hoạch chi tiết tại [plan-assets-qa-and-dispatcher-refactor.md](file:///C:/Users/tuanlee/.gemini/antigravity/brain/49cdbe24-2f1a-40ae-93ac-f41634ec41db/plan-assets-qa-and-dispatcher-refactor.md).

---

## 📋 3. Backlog: NHIỆM VỤ CẦN LÀM TIẾP KHI QUAY LẠI

### Hạng mục 1: Thu hồi ảnh S056 từ Google Flow Account #2
- [ ] Kết nối CDP vào Chrome Account #2 (port 9224).
- [ ] Trích xuất ảnh `S056-A_6s_IMG.png` đã được sinh trên canvas (bàn để các phong bì tiền mặt dán nhãn 'Ăn uống', 'Tiền nhà' ngăn nắp).
- [ ] Lưu vào `assets/` thay thế cho fallback `master_anchor.png` hiện tại.
- [ ] Chạy `stamp_badge_pill.py` cho `S056-A_6s_IMG.png`.

### Hạng mục 2: Tái cấu trúc mã nguồn Dispatcher & QA
- [ ] Cập nhật `tools/flow-dispatcher/flow_dispatcher.py` và `browser_flow.py` sang cơ chế **1-by-1 tuần tự**:
  - Gửi prompt 1 scene $\rightarrow$ Chờ hoàn tất $\rightarrow$ Tải về $\rightarrow$ Kích hoạt QA.
  - Tích hợp chính sách Retry tối đa 1 lần + ghi `failed_assets_review.json`.
- [ ] Nâng cấp `tools/qa/asset_qa_verifier.py`:
  - Thêm tầng kiểm tra Vision QA (đối chiếu `Visual concept` trong `script.md` + quét dị tật cơ thể/tay chân đứt lìa).

### Hạng mục 3: Sinh 5 phân cảnh AIV mới (Storyboard $\rightarrow$ AIV)
- [ ] **Account 3** (Port 9225):
  - `S007`: Storyboard MC bước ra $\rightarrow$ Sinh video AIV Veo.
  - `S011`: Storyboard nhân vật hoảng hốt nhìn sao kê 15 triệu đỏ rực $\rightarrow$ Sinh video AIV Veo.
- [ ] **Account 4** (Port 9226):
  - `S052`: Storyboard Người A mất ngủ, ánh sáng xanh điện thoại $\rightarrow$ Sinh video AIV Veo.
  - `S058`: Storyboard Người B (Nữ) tự tin ghi chép sổ chi tiêu $\rightarrow$ Sinh video AIV Veo.
- [ ] **Account 5** (Port 9227):
  - `S081`: Storyboard nhân vật đứng trên đỉnh đồi lộng gió (khắc phục lỗi tay đứt lìa) $\rightarrow$ Sinh video AIV Veo.

### Hạng mục 4: QA Tổng duyệt & Cập nhật Props Remotion
- [ ] Chạy lại toàn bộ bộ kiểm tra tự động `asset_qa_verifier.py` (đạt 100% PASS trên cả 6 tầng).
- [ ] Đồng bộ composition props sang `studio/remotion/current_props.json`.
- [ ] Render Still Preview tại các phân cảnh mới và sẵn sàng lệnh xuất video master `final_video.mp4`.
