# 🎬 HỆ THỐNG 20/20 CODE-DRIVEN MOTION & VIDEO RENDERING STACK

Tài liệu tham chiếu chuyên sâu dành cho Agent để thiết kế, lập trình và render video tự động bằng code (Zero AI Credit) kết hợp hoàn hảo với giọng đọc Audio-First.

---

## 🧭 TỔNG QUAN BẢN ĐỒ 20/20 CÔNG NGHỆ

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                           20/20 VIDEO CREATIVE STACK                            │
├─────────────────┬─────────────────┬──────────────────┬───────────────────────────┤
│ I. 3 SKILLS     │ II. THIẾT KẾ    │ III. HOẠT ẢNH    │ IV. DỰNG 2D               │
│ 1. Remotion     │ 4. SVGO         │ 6. GSAP          │ 11. Remotion (React)      │
│ 2. Motion AI    │ 5. Satori (JSX) │ 7. Anime.js      │ 12. Motion Canvas (TS)    │
│ 3. GSAP Skill   │                 │ 8. Motion (React)│                           │
│                 │                 │ 9. Rive          ├───────────────────────────┤
│                 │                 │ 10. Lottie       │ V. DỰNG 3D                │
├─────────────────┴─────────────────┴──────────────────┤ 13. Three.js              │
│ VI. ÂM THANH & XUẤT VIDEO                            │ 14. React Three Fiber     │
│ 18. Howler.js (Audio/SFX)                            │ 15. Drei (R3F Helper)     │
│ 19. Mediabunny (In-browser encode)                   │ 16. Rapier (Vật lý 3D)    │
│ 20. FFmpeg (Muxing / Export Final MP4)               │ 17. Postprocessing (Bloom)│
└──────────────────────────────────────────────────────┴───────────────────────────┘
```

---

## I. 3 SKILL DẠY AI CÁCH DỰNG VIDEO

### 1. Remotion Skill (Core React Video Architecture)
- **Bản chất**: Biến React Component thành từng frame video (Frame-based Rendering).
- **Cú pháp then chốt**:
  - `useCurrentFrame()`, `useVideoConfig()`: Lấy frame hiện tại và thông số fps, width, height.
  - `interpolate(frame, [inStart, inEnd], [outStart, outEnd], { extrapolateRight: "clamp" })`: Ánh xạ frame sang giá trị thuộc tính (opacity, scale, x, y).
  - `spring({ frame, fps, config: { damping: 12, mass: 0.5, stiffness: 100 } })`: Tạo chuyển động vật lý đàn hồi cực mượt.
  - `<Sequence from={0} durationInFrames={120}>`: Phân bổ thời lượng scene.
  - `<Audio src={...} volume={...} />`: Đồng bộ âm thanh theo frame.

### 2. Motion AI Kit (Declarative React Motion)
- **Bản chất**: Dùng `motion` (tên mới của Framer Motion) cho các hoạt ảnh UI, Text, Layout.
- **Cú pháp then chốt**:
  - `<motion.div animate={{ scale: [1, 1.2, 1], opacity: 1 }} transition={{ duration: 0.8 }} />`
  - `AnimatePresence`: Điều khiển hiệu ứng biến mất khi đổi cảnh.
  - `variants`: Định nghĩa sẵn các trạng thái chuyển động (hidden, visible, exit) để code đồng bộ và sạch.

### 3. GSAP Skill (Timeline Animation Master)
- **Bản chất**: Điều khiển timeline đa luồng phức tạp, micro-timing chính xác từng mili-giây.
- **Cú pháp then chốt**:
  - `gsap.timeline({ paused: true })`: Tạo trục thời gian độc lập.
  - `tl.to(".box", { x: 200, duration: 1, ease: "power3.out" }, "+=0.2")`: Ghép chuỗi hành động nối tiếp hoặc song song.
  - `stagger: 0.1`: Tạo hiệu ứng gợn sóng xuất hiện lần lượt cho danh sách phần tử.

---

## II. THIẾT KẾ VỚI SVG & JSX

### 4. SVGO (SVG Optimizer)
- **Vai trò**: Tự động dọn dẹp, nén và chuẩn hóa mã SVG (loại bỏ metadata rác của Illustrator/Figma, thu gọn path, clean id).
- **Ứng dụng**: Làm sạch icon tài chính (tiền, thẻ tín dụng, mũi tên) trước khi đưa vào animate để giảm tải CPU render.

### 5. Satori (HTML/JSX to SVG)
- **Vai trò**: Cho phép viết thẻ HTML/JSX TailwindCSS bình thường, sau đó chuyển đổi tức thì thành file Vector SVG sắc nét ở mọi độ phân giải (1080p, 4K).
- **Ứng dụng**: Tự động sinh bảng so sánh tài chính, infographic thẻ ngân hàng, bảng tính lãi suất từ code JSX.

---

## III. 5 THƯ VỊỆN HOẠT ẢNH CHUYÊN BIỆT

| Thư viện | Thế mạnh vượt trội | Khi nào Agent dùng? |
|---|---|---|
| **6. GSAP** | Timeline phức tạp, nối tiếp nhiều hiệu ứng mượt mà | Biểu đồ tăng trưởng tài chính, chuỗi dữ liệu nhiều bước |
| **7. Anime.js** | Nhẹ, cực mạnh về SVG stroke animation & morphing | Hiệu ứng vẽ nét viền SVG, biến hình icon (morphing) |
| **8. Motion** | Animation declarative theo state React | Các card thông tin, pop-up text, badge nổi bật |
| **9. Rive** | Animation tương tác có State Machine | Nhân vật hoạt hình đổi biểu cảm (vui ↔ sốc ↔ tự tin) |
| **10. Lottie** | Phát file JSON animation xuất từ After Effects | Các sticker tiền vàng nổ tung, confetti, icon chuông thông báo |

---

## IV. DỰNG 2D (CODE SANG KHUNG HÌNH)

### 11. Remotion (React Framework for Video)
- Khung sườn chính kết nối toàn bộ 20 công cụ: Quản lý Timeline tổng thể của video, đặt vị trí âm thanh, phụ đề karaoke và các visual sequence.

### 12. Motion Canvas (Procedural Animation in TypeScript)
- **Thế mạnh**: Chuyên trị video giải thích (explainer video), lập trình toán học, đồ thị hàm số, biểu diễn thuật toán theo phong cách 3Blue1Brown.
- **Ứng dụng**: Giải thích công thức lãi kép, toán chi phí cơ hội 10 năm một cách trực quan hoàn hảo.

---

## V. DỰNG 3D (KHÔNG GIAN, VẬT LÝ, HIỆU ỨNG ĐIỆN ẢNH)

### 13. Three.js
- Thư viện WebGL cốt lõi để vẽ hình khối, bề mặt chất liệu, camera 3D và nguồn sáng.

### 14. React Three Fiber (R3F)
- Đưa Three.js vào thế giới React declarative: `<Canvas><mesh><boxGeometry /><meshStandardMaterial /></mesh></Canvas>`.

### 15. Drei (Helper Suite cho R3F)
- Cung cấp component 3D sẵn dùng: `<Text3D>`, `<Float speed={2} rotationIntensity={1}>`, `<Environment preset="city" />`, `<PresentationControls>`.

### 16. Rapier (@react-three/rapier)
- Mô phỏng động lực học vật lý 3D thời gian thực (RigidBody, trọng lực, ma sát, va chạm).
- **Ứng dụng**: Hàng trăm đồng tiền vàng rơi từ trên trời xuống va chạm nảy tưng bừng trên mặt bàn, thẻ tín dụng vỡ vụn khi rơi xuống đất.

### 17. Postprocessing (@react-three/postprocessing)
- Áp bộ lọc điện ảnh lên canvas 3D:
  - `<Bloom luminanceThreshold={0.2} intensity={1.5} />`: Tạo hiệu ứng neon phát sáng công nghệ.
  - `<DepthOfField focusDistance={0.02} focalLength={0.5} bokehScale={3} />`: Xóa phông mờ ảo.
  - `<Vignette darkness={0.5} />`: Bo tối 4 góc tăng độ kịch tính.

---

## VI. ÂM THANH VÀ XUẤT VIDEO HOÀN CHỈNH

### 18. Howler.js
- Bộ điều khiển âm thanh độc lập: Xử lý nhạc nền (BGM) tự động giảm âm lượng (audio ducking) khi có giọng đọc, kích hoạt sound effects (SFX tiếng ting ting, tiếng nổ, tiếng gõ phím) chính xác theo frame.

### 19. Mediabunny
- Công cụ encode video thế hệ mới chạy WebAssembly/WebCodecs, cho phép xem trước và xuất video cực nhanh.

### 20. FFmpeg
- Trạm ghép nối cuối cùng: Trộn tracks video Remotion + audio narration VieNeu-TTS + nhạc nền Howler + subtitle karaoke vào 1 file **`output_final.mp4`** (H.264/AAC) đạt chuẩn 1080p 60fps để tải lên YouTube.

---

## 🎯 CÁCH AGENT ÁP DỤNG TRONG GIAI ĐOẠN PHASE 5

Khi user duyệt B-roll Plan (`@approve-broll`), Agent sẽ tự động sinh mã hoặc cấu trúc props cho các cảnh:
1. **Nếu là `AIV`**: Xuất Storyboard + Prompt tạo video AI (Veo/Kling/Runway).
2. **Nếu là `IMG`**: Xuất Prompt ảnh tĩnh chất lượng cao + Props Ken Burns chuyển động camera cho Remotion.
3. **Nếu là `GFX`**: Xuất code Component chuẩn sử dụng 20/20 Stack trên (Remotion + Motion / R3F / GSAP) để render tự động với **0 credit AI**!
