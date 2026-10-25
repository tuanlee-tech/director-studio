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
| **`@start-tts`** | `@start-tts` | Khởi động dịch vụ VieNeu-TTS |
| **`@stop-tts`** | `@stop-tts` | Tắt dịch vụ VieNeu-TTS |
| **`@new-channel`** | `@new-channel my-channel` | Tạo kênh mới với cấu trúc thư mục chuẩn |
| **`@set-channel`** | `@set-channel my-channel` | Chọn kênh đang làm việc |
| **`@new-video`** | `@new-video "AI thay đổi giáo dục"` | Tạo video mới (tự tạo thư mục slug sạch) |
| **`@gen-script`** | `@gen-script "Chủ đề video" -minutes 8` | Tạo kịch bản chuẩn beat structure |
| **`@show-script`** | `@show-script` | Xem nội dung kịch bản hiện tại |
| **`@edit-scene`** | `@edit-scene 3 "Lời đọc mới..."` | Sửa lời đọc của một scene |
| **`@set-voice`** | `@set-voice "Hải Đăng"` | Đổi giọng đọc mặc định (`Hải Đăng`, `Binh`, `Ngoc`...) |
| **`@set-pace`** | `@set-pace 4` | Đặt tốc độ đọc chuẩn (từ/giây) |
| **`@set-tts`** | `@set-tts vieneu` | Đổi engine đọc (`vieneu`, `gemini-3.8`) |
| **`@gen-audio`** | `@gen-audio -scene 1` | Tạo file audio `.wav` cho 1 cảnh |
| **`@gen-all-audio`**| `@gen-all-audio` | Tạo audio tự động cho TOÀN BỘ kịch bản |
| **`@play`** | `@play 1` | Mở nghe thử file audio của cảnh 1 |
| **`@analyze`** | `@analyze --all` | Dùng Whisper lấy mốc thời gian từng từ |
| **`@timing`** | `@timing -scene 1` | Xem bảng thời gian chi tiết từng từ |
| **`@plan-broll`** | `@plan-broll` | Tự động phân tích và chia số lượng B-roll |
| **`@show-broll`** | `@show-broll` | Xem bảng kế hoạch B-roll để kiểm tra |
| **`@edit-broll`** | `@edit-broll S003 duration 6s` | Chỉnh sửa B-roll (thời lượng, góc máy, loại) |
| **`@approve-broll`**| `@approve-broll` | **Duyệt B-roll** (Cổng kiểm duyệt trước khi sinh hình) |
| **`@gen-prompts`** | `@gen-prompts --all` | Tạo bảng prompt ảnh + video + storyboard |
| **`@show-prompts`** | `@show-prompts` | Xem bảng prompts theo định dạng shot list |
| **`@shot-list`** | `@shot-list` | Xuất file shot list đầy đủ |
| **`@gen-subs`** | `@gen-subs --format srt` | Sinh phụ đề karaoke `.srt` hoặc `.ass` |
| **`@preview-subs`** | `@preview-subs` | Xem thử phụ đề khớp từng từ trong chat |
| **`@schedule`** | `@schedule show` | Xem lịch trình các video (⬜ Chưa làm / ✅ Đã xong) |
| **`@pipeline`** | `@pipeline` | Chạy tự động toàn bộ luồng sản xuất |
| **`@next`** | `@next` | Đi tiếp bước tiếp theo |
| **`@undo`** | `@undo` | Quay lại bước trước đó |

---

## 🎯 Quy trình 7 bước chuẩn làm 1 video

1. **Bước 1**: `@set-channel <tên-kênh>`
2. **Bước 2**: `@new-video "<tiêu đề video>"`
3. **Bước 3**: `@gen-script "<chủ đề>"`
4. **Bước 4**: `@gen-all-audio` *(tạo giọng đọc audio-first)*
5. **Bước 5**: `@analyze --all` *(Whisper đo chính xác từng từ)*
6. **Bước 6**: `@plan-broll` → `@approve-broll` *(duyệt kế hoạch hình ảnh)*
7. **Bước 7**: `@gen-prompts --all` & `@gen-subs` *(nhận prompt tạo video + file phụ đề karaoke)*

---

## 💡 Mẹo sử dụng
- Nếu máy chưa bật VieNeu-TTS, bạn chỉ cần gõ `@start-tts`.
- Khi bán bộ skill này cho người dùng, họ chỉ cần đọc trang Cheatsheet này là có thể vận hành 100% bằng chat với AI.
