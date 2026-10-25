# ⚡ Bảng tra cứu Cheatcode — Video Director Skill

Lớp **Cheatcode API** cho phép bạn điều khiển Agent bằng các lệnh ngắn gọn bắt đầu bằng dấu `@` trực tiếp trong ô chat. Bạn **không cần** mở PowerShell, Bash hay gõ bất kỳ câu lệnh terminal phức tạp nào. Agent sẽ tự động nhận diện hệ điều hành (Windows/Linux) và tự động thực thi.

---

## 📌 Bảng tra cứu nhanh (Quick Reference)

| Lệnh Cheatcode | Cú pháp ví dụ | Mô tả chức năng |
|---|---|---|
| **`@help`** | `@help audio` | Xem hướng dẫn chi tiết theo nhóm hoặc lệnh |
| **`@cheatsheet`** | `@cheatsheet` | Mở bảng tóm tắt cheatcode |
| **`@status`** | `@status` | Xem tổng quan trạng thái kênh, video, dịch vụ |
| **`@health`** | `@health` | Kiểm tra tình trạng TTS, Whisper, Studio |
| **`@start-container`** | `@start-container` | Khởi động container project (Docker Compose tự detect GPU/CPU) |
| **`@stop-container`** | `@stop-container` | Dừng toàn bộ container của project |
| **`@status-container`**| `@status-container`| Xem trạng thái các container đang chạy trong project |
| **`@start-tts`** | `@start-tts` | Khởi động dịch vụ VieNeu-TTS Native (Python/uv) |
| **`@stop-tts`** | `@stop-tts` | Tắt dịch vụ VieNeu-TTS Native |
| **`@new-channel`** | `@new-channel my-channel` | Tạo kênh mới với cấu trúc thư mục chuẩn |
| **`@set-channel`** | `@set-channel my-channel` | Chọn kênh đang làm việc |
| **`@new-video`** | `@new-video "AI thay đổi giáo dục"` | Tạo video mới (tự tạo thư mục slug sạch) |
| **`@gen-script`** | `@gen-script "Chủ đề video" -minutes 8` | Tạo kịch bản chuẩn beat structure |
| **`@show-script`** | `@show-script` | Xem nội dung kịch bản hiện tại |
| **`@edit-scene`** | `@edit-scene 3 "Lời đọc mới..."` | Sửa lời đọc của một scene |
| **`@set-voice`** | `@set-voice "Hải Đăng"` | Đổi giọng đọc mặc định (`Hải Đăng`, `Binh`, `Ngoc`...) |
| **`@set-pace`** | `@set-pace 4` | Đặt tốc độ đọc chuẩn (từ/giây) |
| **`@set-tts`** | `@set-tts vieneu` | Đổi engine đọc (`vieneu`, `gemini-3.8`) |
| **`@set-strategy`** | `@set-strategy hybrid` | Đổi chiến lược asset: `hybrid` (tiết kiệm), `all-aiv` |
| **`@gen-audio`** | `@gen-audio -scene 1` | Tạo file audio `.wav` cho 1 cảnh |
| **`@gen-all-audio`**| `@gen-all-audio` | Tạo audio tự động cho TOÀN BỘ kịch bản |
| **`@play`** | `@play 1` | Mở nghe thử file audio của cảnh 1 |
| **`@analyze`** | `@analyze --all` | Dùng Whisper lấy mốc thời gian từng từ |
| **`@timing`** | `@timing -scene 1` | Xem bảng thời gian chi tiết từng từ |
| **`@plan-broll`** | `@plan-broll` | Tự động phân tích và chia số lượng B-roll |
| **`@show-broll`** | `@show-broll` | Xem bảng kế hoạch B-roll để kiểm tra |
| **`@edit-broll`** | `@edit-broll S003 duration 6s` | Chỉnh sửa B-roll (thời lượng, góc máy, loại) |
| **`@approve-broll`**| `@approve-broll` | **Duyệt B-roll** (Cổng kiểm duyệt trước khi sinh hình) |
| **`@test-style`** | `@test-style` | **Tạo thử 1 ảnh** trên Google Flow để kiểm tra phong cách thực tế |
| **`@lock-style`** | `@lock-style` | **Khóa Style Lock** sau khi đã test ảnh thành công trên Google Flow |
| **`@gen-prompts`** | `@gen-prompts --all` | Tạo bảng prompt ảnh + video + storyboard hàng loạt (sau khi lock style) |
| **`@show-prompts`** | `@show-prompts` | Xem bảng prompts theo định dạng shot list |
| **`@shot-list`** | `@shot-list` | Xuất file shot list đầy đủ |
| **`@gen-remotion`** | `@gen-remotion` | Xuất file composition Remotion để render tự động |
| **`@preview-video`**| `@preview-video` | **Xem trước timeline** và Remotion Player trong Studio (port 3000) |
| **`@render-video`** | `@render-video` | **Render xuất video MP4** tự động 100% bằng Remotion Engine (H.264 1080p) |
| **`@render-code-motion`** | `@render-code-motion S005` | Tạo component TSX (20/20 Stack) cho cảnh đồ họa chuyển động |
| **`@list-motion-stack`** | `@list-motion-stack` | Liệt kê chi tiết 20/20 công cụ dựng hoạt ảnh & video bằng code |
| **`@gen-subs`** | `@gen-subs --format srt` | Sinh phụ đề karaoke `.srt` hoặc `.ass` |
| **`@preview-subs`** | `@preview-subs` | Xem thử phụ đề khớp từng từ trong chat |
| **`@schedule`** | `@schedule show` | Xem lịch trình các video (⬜ Chưa làm / ✅ Đã xong) |
| **`@pipeline`** | `@pipeline` | Chạy tự động toàn bộ luồng sản xuất |
| **`@next`** | `@next` | Đi tiếp bước tiếp theo |
| **`@undo`** | `@undo` | Quay lại bước trước đó |

---

## 🎯 Quy trình 8 bước chuẩn làm 1 video

1. **Bước 1**: `@set-channel <tên-kênh>`
2. **Bước 2**: `@new-video "<tiêu đề video>"`
3. **Bước 3**: `@gen-script "<chủ đề>"`
4. **Bước 4**: `@gen-all-audio` *(tạo giọng đọc audio-first)*
5. **Bước 5**: `@analyze --all` *(Whisper đo chính xác từng từ)*
6. **Bước 6**: `@plan-broll` → `@approve-broll` *(duyệt kế hoạch hình ảnh)*
7. **Bước 7 (Style Prototyping Gate)**: `@test-style` *(tạo thử 1 ảnh trên Google Flow để kiểm tra phong cách thực tế)* → nếu đẹp thì gõ `@lock-style` để chốt!
8. **Bước 8**: `@gen-prompts --all`, `@render-code-motion` & `@gen-subs` *(sinh toàn bộ prompt đã chốt style + code motion graphics + phụ đề karaoke)*

---

## 🎨 Cổng Thử Nghiệm Phong Cách (Style Prototyping Gate)
Dự kiến trên giấy tờ có thể khác xa khi AI tạo hình thực tế. Trước khi sinh hàng chục prompt hàng loạt:
- Gõ **`@test-style`**: Agent trích xuất 1 prompt tiêu biểu nhất (cảnh Hook).
- Dán vào **Google Flow / Midjourney / Flux** để sinh thử 1 ảnh.
- Tinh chỉnh prompt nếu cần (`sửa style: ...`).
- Khi ảnh thực tế đã chuẩn gu, gõ **`@lock-style`**: Toàn bộ các cảnh sau sẽ được sinh theo Style Lock đã được kiểm chứng thực tế!

---

## 🚀 Hệ Thống 20/20 Code-Driven Motion & Video Rendering Stack
Hỗ trợ Agent viết code render video và hoạt ảnh với **0 chi phí AI Credit**:
- **I. 3 Skills cốt lõi**: Remotion Skill (React video frame-by-frame), Motion AI Kit (micro-animations), GSAP Skill (timeline chính xác từng frame).
- **II. Thiết kế Vector**: SVGO (tối ưu hóa SVG), Satori (biến JSX/Tailwind thành SVG sắc nét).
- **III. 5 Thư viện hoạt ảnh**: GSAP, Anime.js (SVG stroke & morphing), Motion, Rive (interactive state machine), Lottie (AE stickers).
- **IV. Dựng 2D**: Remotion (ghép React component thành MP4), Motion Canvas (video giải thích/toán học).
- **V. Dựng 3D**: Three.js, React Three Fiber (R3F), Drei (3D helpers), Rapier (vật lý 3D va chạm, rơi tự do), Postprocessing (Bloom phát sáng neon, xóa phông).
- **VI. Âm thanh & Xuất video**: Howler.js (BGM ducking & SFX), Mediabunny (in-browser encoding), FFmpeg (ghép xuất MP4 chuẩn 1080p).
- Tra cứu nhanh: Gõ **`@list-motion-stack`**.

---

## 💰 Chiến lược Hybrid Asset — Tiết kiệm 70%–85% Credit AI
1. **30 giây đầu (Hook)**: Dùng **AIV (AI Video)** để níu chân người xem ở thời điểm quyết định của thuật toán YouTube.
2. **Sau 30 giây (Thân bài)**:
   - **GFX (Motion Graphic bằng Remotion/Hyperframe)**: Số liệu, biểu đồ, so sánh cột, đồng hồ chạy tiền → Vẽ bằng code React/SVG (**0 credit AI**).
   - **IMG (Ảnh tĩnh AI + Remotion Motion)**: Minh họa bối cảnh, nhân vật → Ảnh tĩnh chi phí cực rẻ kết hợp hiệu ứng camera mượt mà (Ken Burns, Pan, Zoom).
   - **`@gen-remotion`**: Tự động xuất file composition để render video bằng code.

---

## 💡 Mẹo sử dụng
- **Chạy bằng Container (Docker)**: Gõ `@start-container` — tự động phát hiện GPU/CPU để khởi động toàn bộ cụm VieNeu-TTS (7860 & 8000) và Studio UI (3000). Dừng lại bằng `@stop-container`.
- **Chạy trực tiếp Native (không cần Docker)**: Gõ `@start-tts` (Windows/Linux đều hỗ trợ qua launcher native Python/uv).
- Khi bán bộ skill này cho người dùng, họ chỉ cần đọc trang Cheatsheet này là có thể vận hành 100% bằng chat với AI.
