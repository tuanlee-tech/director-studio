---
always_on: true
description: "Bộ 8 Quy Tắc Bắt Buộc Tuân Thủ Toàn Diện Khi Thao Tác Remotion & Motion Graphics (Mandatory Remotion & GFX Motion Rules)"
---

# BỘ QUY TẮC BẮT BUỘC TUÂN THỦ TOÀN DIỆN KHI THAO TÁC REMOTION & MOTION GRAPHICS
*(MANDATORY REMOTION & GFX MOTION PRODUCTION RULES)*

> [!IMPORTANT]
> **Đây là quy chuẩn tối thượng, bất biến và bắt buộc tuân thủ 100% đối với mọi tác vụ thiết kế, viết mã, sinh kịch bản, và tinh chỉnh cảnh (scenes) Remotion trong toàn bộ dự án.**
> **Không có bất kỳ ngoại lệ nào.**

---

## 🎨 8 Điều Luật Bất Biến Khi Tạo & Dựng Cảnh Remotion

### ĐIỀU 1: 100% Visual Vector Graphic Cho Mọi Cảnh GFX (Nghiêm Cấm Plain-Text Fallback)
1. Mọi cảnh dạng `GFX` hoặc `MotionGraphic` phải được hiện thực hóa thành **hình ảnh minh họa trực quan sinh động** (Vector SVG, biểu đồ động, timeline slider, sơ đồ phân luồng, mô hình 3D, mockup app, v.v.).
2. **Tuyệt đối nghiêm cấm**:
   - Không được để cảnh GFX chỉ là một chiếc hộp đen/card chứa text mô tả trừu tượng hoặc alt-text.
   - Không được dùng emoji đơn điệu (như biểu tượng `💰`) để thay thế cho đồ họa thực thụ.
   - Không được để bất kỳ cảnh GFX nào rơi vào khối `fallback` mặc định. Toàn bộ cảnh GFX trong video phải có handler chuyên biệt (100% coverage).

---

### ĐIỀU 2: Tuyệt Đối Không Để Lộ Component Name & Dev Prefix Lên Khung Hình
1. **Nghiêm cấm hiển thị tên component, tên file, hoặc tiền tố kỹ thuật** lên màn hình video:
   - Các tiền tố như `ChartMotion: `, `SplitComparison: `, `AlertBox: `, `FocusCard: `, `CounterNumber: `, `LoopDiagram: `, `TreeGrowth: `, `IntroCard: `, `BarChart: `, `PieChart: `, `TimelineSlider: `, `Infographic: `, `CalendarAnimation: `, `StackFee: `, `DrainWater: `, `MonthCalendar: `, `CreditScoreMeter: `, `BadgeGraphic: `, `ComparisonTable: `, `ProgressBar: `, `MilestoneUnlocked: `, `StepFlow: `, `StepHeader: `, `AppUnlink: `, `TargetHighlight: `, `BadgeUnlock: `, `SalarySplit: `, `BudgetEnvelope: `, `CountdownMonths: `, `AssetTree: `... phải bị triệt tiêu hoàn toàn.
2. Tiêu đề hiển thị trên video phải là **tiêu đề người xem thực tế** (*viewer-facing headline*), bằng tiếng Việt tự nhiên, gãy gọn, chuẩn ngữ pháp.
3. Luôn bọc qua hàm xử lý `cleanText()` ở tầng component React và làm sạch dữ liệu nguồn trong `remotion-composition.json` và `current_props.json`.

---

### ĐIỀU 3: Chống Hardcode Lặp Lại Component Không Hợp Ngữ Cảnh
1. Mỗi cảnh phải thể hiện đúng bản chất của số liệu và tình huống tài chính:
   - **S018**: Đồ thị dốc đứng nợ tăng vọt (15tr $\rightarrow$ 40tr).
   - **S027**: Biểu đồ so sánh cột 6% vay mua nhà vs 35% thẻ tín dụng.
   - **S030**: Đường dư nợ gốc 40 triệu **nằm ngang phẳng lì suốt 12 tháng** (chứng minh trả tối thiểu nợ gốc không giảm).
   - **S034**: Đồ thị kép Lãi kép Đầu tư (Xanh vút lên) vs Lãi kép Vay nợ (Đỏ cắm dốc xuống).
2. **Tuyệt đối không lặp lại**: Không bao giờ được dùng lại biểu đồ cột 6% vs 35% cho các cảnh nói về đường nằm ngang, đồ thị dốc hay các phân tích khác.

---

### ĐIỀU 4: Khớp 100% Nội Dung Visual Với Lời Thoại Narration Tại Frame Đó
1. Hình ảnh hiển thị tại frame $F$ phải bổ trợ chính xác cho câu thoại của người thuyết minh tại frame $F$.
2. Không bao giờ hiển thị nội dung của cảnh sau cho cảnh trước (ví dụ: đang đọc câu thoại *“Khi đầu tư, lãi kép...”* ở S034 thì tuyệt đối không được hiển thị bảng 45 ngày của S035).

---

### ĐIỀU 5: Bố Cục Rời Rạc Chống Đè Chữ (Decoupled Layout — Anti-Collision)
1. **Khoảng cách an toàn (Headroom & Margin)**:
   - Tag phân loại cách Tiêu đề: `marginBottom: 16px - 20px`.
   - Tiêu đề cách Khối đồ họa: `marginBottom: 24px - 36px`.
   - Vùng chứa đồ họa (*graphic container*): chiều cao tối thiểu $\ge 260px - 320px$.
2. **Chống va chạm nhãn (Label Decoupling)**:
   - Các nhãn mốc thời gian (như `NGÀY 01`, `NGÀY 45`, `Thiếu 1.000đ`) phải được bố trí thông thoáng, nằm riêng biệt ở phía trên hoặc phía dưới trục timeline/thanh bar, **tuyệt đối không đè lấn hoặc che khuất thanh motion graphic**.
   - Con số trên cột biểu đồ (ví dụ: `35% / Năm!`) phải có khoảng đệm tối thiểu 24px với đỉnh cột và không bao giờ chạm vào tiêu đề.

---

### ĐIỀU 6: Subtitle Karaoke Trong Suốt 100% (Borderless Glassy Subtitle)
1. Subtitle tuyệt đối không sử dụng hộp nền đen đặc hoặc viền hộp dày cộp che khuất nội dung hình ảnh video.
2. Sử dụng nền trong suốt 100% (`backgroundColor: 'transparent'`, `border: 'none'`).
3. Làm nổi bật chữ bằng kỹ thuật đổ bóng chữ đa tầng (*multi-layer outline text-shadow*):
   ```css
   text-shadow: 0 2px 6px rgba(0,0,0,0.95), 0 0 12px rgba(0,0,0,0.9), -2px -2px 0 rgba(0,0,0,0.9), 2px -2px 0 rgba(0,0,0,0.9), -2px 2px 0 rgba(0,0,0,0.9), 2px 2px 0 rgba(0,0,0,0.9);
   ```
4. Khoảng cách giữa các từ vừa phải, cân đối; số tiền tự động format định dạng tiền tệ Việt Nam (`đ`, `VNĐ`).

---

### ĐIỀU 7: Cô Lập Mẫu Kênh Tuyệt Đối (Strict Channel Isolation)
1. Mọi thành phần hiển thị, typography, subtitle và theme màu sắc của từng kênh phải nằm độc lập bên trong `channels/<channel_id>/template/`.
2. Router `Root.tsx` điều phối kênh qua props `channel`. Khi chỉnh sửa hoặc sản xuất video cho kênh này, tuyệt đối không gây ảnh hưởng hay conflict tới các kênh khác.

---

### ĐIỀU 8: Quy Trình Kiểm Tra Bắt Buộc (Automated Audit Verification)
Trước khi bàn giao hoặc hoàn tất bất kỳ tác vụ nào liên quan đến Remotion/GFX, bắt buộc phải:
1. Chạy công cụ kiểm tra tự động:
   ```bash
   python tools/audit_remotion_gfx.py
   ```
   Kết quả bắt buộc phải đạt **`[PASS] AUDIT PASSED! 100% compliant with Remotion Motion Rules`**.
2. Render kiểm thử hình ảnh (*still render*) tại các phân cảnh vừa can thiệp để đảm bảo không lỗi biên dịch, không lỗi font, và bố cục hiển thị chuẩn mực trước khi xuất video.
