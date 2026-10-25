---
name: remotion-motion-master
description: >-
  Bộ 20 kỹ năng, thư viện & công nghệ chuẩn mực để thiết kế và dựng video Remotion chuyên nghiệp:
  GSAP, Motion (Framer Motion), Anime.js, SVGO, Satori, Three.js, React Three Fiber,
  Drei, Rapier 3D physics, Postprocessing, Lottie, Rive, Motion Canvas, Howler.js,
  Mediabunny, FFmpeg. Luôn áp dụng khi tạo và tinh chỉnh các scene Remotion motion graphics.
---

# 🎬 Remotion Motion Master — 20 Kỹ Năng & Thư Viện Đỉnh Cao Cho Video Motion Graphics

Quy chuẩn tối thượng để AI thiết kế, viết mã và dựng các cảnh (scenes) Motion Graphics, Visual Infographics, 2D/3D Animation trên nền tảng Remotion. Luôn áp dụng bộ quy tắc này cho mọi component và template video.

---

## I. 3 Kỹ Năng Dạy LLM Dựng Video Chuẩn Mực

### 1. Remotion Skills (Quy chuẩn Frame-Based của Remotion)
- **Tuyệt đối không dùng thời gian thực `setTimeout` / `setInterval`**: Mọi chuyển động phải là hàm số của `useCurrentFrame()`.
- **Nội suy chuyển động**:
  - Dùng `interpolate(frame, [start, end], [valStart, valEnd], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.bezier(...) })`.
  - Dùng `spring({ frame, fps, config: { damping: 14, mass: 0.8, stiffness: 120 } })` cho các hiệu ứng nảy, xuất hiện card, số nhảy.
- **Tách Layer & Sequence**:
  - Dùng `<Sequence from={...} durationInFrames={...}>` để phân tách từng cảnh.
  - Dùng `<Loop durationInFrames={...}>` cho background animation lặp vô tận (hạt bụi, sóng, BGM).
  - Tránh rerender nặng: Đưa các tính toán phức tạp ra ngoài hoặc dùng `useMemo`.

### 2. Motion AI Kit (Framer Motion trong Remotion)
- Khi dùng `framer-motion` trong Remotion:
  - Đồng bộ với frame bằng cách tính `custom` props hoặc biến CSS dựa trên `useCurrentFrame()`.
  - Sử dụng các preset hoạt ảnh: `initial={{ opacity: 0, scale: 0.8, y: 30 }}`, `animate={{ opacity: 1, scale: 1, y: 0 }}`.
  - Dùng `layout` và `AnimatePresence` để chuyển đổi mượt mà giữa các trạng thái số liệu hoặc danh sách.

### 3. GSAP Skill (Timeline & Complex Choreography)
- Tạo GSAP timeline không chạy tự động (`paused: true`).
- Đồng bộ timeline theo Remotion frame:
  ```ts
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  useEffect(() => {
    tl.seek(frame / fps);
  }, [frame, fps]);
  ```
- Dùng GSAP cho các chuỗi chuyển động phức tạp nhiều phần tử (staggered nodes, vẽ đường cong SVG).

---

## II. Thiết Kế Vector & Dynamic Typography

### 4. SVGO (Tối ưu hóa Vector Path)
- Mọi SVG vẽ tay hoặc sinh bằng mã phải có cấu trúc path gọn gàng, tọa độ chuẩn `viewBox="0 0 1000 1000"`.
- Loại bỏ metadata thừa, giữ nguyên `id` và `class` của các nhánh để animate độc lập qua CSS hoặc `strokeDashoffset`.

### 5. Satori (Chuyển JSX/HTML thành SVG động)
- Sử dụng mô hình Flexbox của Satori để tự động dàn trang text dài, badge, thẻ số liệu tài chính thành vector SVG sắc nét mà không lo vỡ chữ hoặc đè heading.

---

## III. 5 Thư Viện Hoạt Ảnh — Mỗi Thứ Một Việc

### 6. GSAP (Timeline mượt, chính xác từng mili-giây)
- Phù hợp nhất cho: Các chuỗi timeline nhiều bước (Step 1 -> Step 2 -> Step 3 -> Step 4), các roadmap ngang, hiệu ứng camera lướt qua các mốc thời gian.

### 7. Anime.js (SVG Path Morphing & Drawing)
- Phù hợp nhất cho: Vẽ đường viền SVG theo nét bút (`strokeDashoffset`), biến hình (morphing) từ hình tròn tiền xu thành hình cây nợ.
- Tính toán: `const progress = interpolate(frame, [0, 45], [1000, 0]); strokeDashoffset: progress`.

### 8. Motion / Framer Motion (Vật lý Spring trong React)
- Phù hợp nhất cho: Các thẻ Card trồi lên, nút bấm phát sáng co giãn, danh sách liệt kê trượt vào (`staggerChildren`).

### 9. Rive (Interactive Animation & State Machines)
- Phù hợp cho các nhân vật hoạt hình 2D có biểu cảm thay đổi theo dữ liệu (nhân vật hoảng hốt khi nợ tăng, tự tin khi trả hết nợ).

### 10. Lottie (Phát Animation After Effects)
- Dùng `@remotion/lottie` để phát các asset vector có sẵn (pháo hoa ăn mừng trả nợ xong, dấu mộc ĐÃ THANH TOÁN dập xuống, chuông cảnh báo lắc lư).

---

## IV. Dựng 2D & Video Giải Thích

### 11. Remotion Core (Video Engine)
- Biến mọi đoạn mã React thành từng frame chuẩn 4K/FullHD 30fps/60fps.
- Tự động tách âm thanh narration, timing karaoke từng từ, ken burns hình ảnh và motion graphic đồng bộ hoàn hảo.

### 12. Motion Canvas (Toán học & Diagram Animation)
- Áp dụng triết lý animation vector toán học: Tọa độ rõ ràng, đường nối spline mượt mà, biểu đồ biến thiên liên tục.

---

## V. Dựng 3D, Ánh Sáng & Vật Lý

### 13. Three.js (3D WebGL trực tiếp)
- Tạo không gian chiều sâu cho video: Sàn phản chiếu, hạt bụi lơ lửng (dust particles), khối hộp lập phương tài chính.

### 14. React Three Fiber (R3F với Remotion)
- Dùng `@remotion/three` tích hợp Canvas 3D vào video composition:
  ```tsx
  import { ThreeCanvas } from "@remotion/three";
  <ThreeCanvas width={1920} height={1080}>
    <ambientLight intensity={0.5} />
    <pointLight position={[10, 10, 10]} />
    <CoinMesh frame={frame} />
  </ThreeCanvas>
  ```

### 15. Drei (Bộ trợ thủ R3F)
- `Float`: Làm đồng tiền xu hoặc thẻ tín dụng 3D bập bênh trong không gian.
- `Text3D`: Tạo chữ 3D nổi bật (`40.000.000 VNĐ`).

### 16. Rapier (Vật lý rơi & va chạm 3D)
- Mô phỏng vật lý chân thực: Hàng chục đồng tiền vàng rơi từ trên trời xuống va chạm vào nhau và chất thành đống khi nói về tích sản.

### 17. Postprocessing (Hiệu ứng hình ảnh cao cấp)
- `Bloom`: Phát sáng neon rực rỡ cho các con số đỏ nguy hiểm `35%` hoặc thẻ nợ.
- `Vignette` & `ChromaticAberration`: Tạo cảm giác điện ảnh cho cảnh báo động tài chính.

---

## VI. Âm Thanh & Xuất Video Đỉnh Cao

### 18. Howler.js (Quản lý Sound FX)
- Kích hoạt SFX đúng frame: Tiếng keng khi số nhảy xong, tiếng còi hú khi hiện AlertBox, tiếng xé giấy khi hủy liên kết thẻ.

### 19. Mediabunny / WebCodecs (Render nhanh trong trình duyệt)
- Tăng tốc preview và render từng phân cảnh ngắn ngay lập tức.

### 20. FFmpeg (Muxing, Master Narration & Encode Hardware)
- Ghép nối audio narration master tránh lỗi Windows CLI overflow.
- Encode chuẩn H.264 / AAC 48kHz bitrate cao, âm thanh đạt chuẩn EBU R128 (-14 đến -23 LUFS).

---

## 🎨 Nguyên Tắc Bất Biến Khi Tạo Scene Remotion

1. **Không Text Trống (No Alt Text Only)**: Tuyệt đối không bao giờ để một cảnh GFX chỉ là một chiếc hộp đen chứa chữ mô tả. Luôn vẽ hình ảnh trực quan (SVG animated tree, bar charts, đồng hồ đếm ngược, biểu đồ pie, thẻ tương tác).
2. **Không Đè Chữ (Decoupled Layout)**: Heading, Subtitle và Con số phải có vùng đệm (`margin`/`gap: 24px+`), chiều cao container biểu đồ phải đủ lớn để cột cao nhất không bao giờ đè vào tiêu đề.
3. **Subtitle Trong Suốt (Borderless Glassy Subtitle)**: Subtitle karaoke không dùng hộp đen đặc che nội dung video; dùng nền trong suốt với text-shadow đa tầng nổi bật trên mọi background.
4. **Đúng Phong Cách Kênh**: Mỗi kênh có Channel Bible và style lock riêng. Toàn bộ component phải nằm độc lập trong `channels/<channel_id>/template/`.
