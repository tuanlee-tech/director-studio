# 🎬 Kế Hoạch: Remotion Video Studio Renderer & Google Flow Multi-Account Dispatcher

> **Tài liệu chốt qua phiên phỏng vấn `/grill-me` ngày 25/10/2026.**  
> Mục tiêu: Hoàn thiện chu trình khép kín từ Audio-First → Tự động tạo Asset đa tài khoản Google Flow → Hậu kỳ dựng video tự động 100% bằng code Remotion / FFmpeg.

---

## 🧭 1. Tổng quan Kiến trúc Hệ thống

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              AI AUDIO & VIDEO MONOREPO                                │
├──────────────────────────┬─────────────────────────────┬───────────────────────────────┤
│ 1. VIE-NEU TTS (8000)    │ 2. STUDIO DASHBOARD (3000)  │ 3. VIDEO DIRECTOR SKILL       │
│ • Hải Đăng 48kHz         │ • Tabs: Dịch vụ & Health   │ • Audio-First 5 Phase         │
│ • Whisper word timing    │ • [MỚI] Tab Video Preview   │ • Cheatcode API (@command)    │
│ • Phụ đề Karaoke         │ • Remotion Player Timeline  │ • 20/20 Motion Graphics Stack │
│                          │ • Nút '🚀 Xuất MP4 Video'   │ • Style Prototyping Gate      │
└──────────────────────────┴──────────────┬──────────────┴───────────────────────────────┘
                                          │
                                          ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ GIAI ĐOẠN 1: HẬU KỲ DỰNG VIDEO TỰ ĐỘNG (REMOTION + FFMPEG RENDERER TRONG STUDIO)       │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ • Giao diện: Tích hợp Remotion Web Player trực tiếp vào Studio (port 3000).            │
│ • Timeline Preview: Xem trước video theo từng visual beat (AIV clip, IMG Ken Burns,   │
│   GFX 20/20 component).                                                                │
│ • Auto-Sync: Ghép audio narration chuẩn frame Whisper, phụ đề karaoke đổi màu từng từ, │
│   BGM ducking tự động hạ âm lượng khi có giọng đọc.                                    │
│ • Xuất bản: 1-click trên Web hoặc gõ cheatcode '@render-video' → Xuất MP4 1080p60fps.  │
└────────────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼ (Giai đoạn tiếp theo)
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ GIAI ĐOẠN 2: GOOGLE FLOW MULTI-ACCOUNT DISPATCHER (CHROME DEBUGGING PROTOCOL - CDP)    │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ • Kiến trúc: Chrome CDP với thư mục profiles độc lập (acc1 → acc5). User login 1 lần.  │
│ • Điều phối Sub-Agents: Mỗi sub-agent gắn vào 1 cửa sổ Chrome qua port debug riêng.   │
│ • Chiến lược Quota:                                                                   │
│   - AIV (tốn credit): Chia đều cho 5 account (tận dụng tối đa 250 credit/ngày).       │
│   - IMG (0 credit - free): Bơm song song batch 3-4 prompt để Google Flow render nhanh. │
│ • Auto-Sync Local: Tự động tải asset về `assets/` và đổi tên đúng chuẩn S###.          │
│ • Phong cách tham khảo: https://github.com/phucnguyentvp1/frameweaver                  │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📌 2. Các Quyết Định Đã Thống Nhất (/grill-me Consensus)

1. **Lộ trình triển khai (Roadmap Priority)**:
   - **Giai đoạn 1 (Làm ngay)**: Tích hợp Module Hậu Kỳ Dựng Video Tự Động (Remotion + FFmpeg Renderer) vào Studio hiện tại để có thể xuất file MP4 hoàn chỉnh từ assets có sẵn.
   - **Giai đoạn 2 (Mở rộng)**: Xây dựng Module Multi-Account Google Flow Dispatcher (Chrome Debugging / CDP đa cửa sổ).

2. **Vị trí và hình thức tích hợp Hậu kỳ**:
   - Thêm Tab mới **"🎬 Video Preview & Timeline"** vào giao diện Web Studio hiện có (`http://localhost:3000`).
   - Nhúng **Remotion Player** để xem trước timeline mượt mà, đổi video qua dropdown.
   - Nút bấm **"🚀 Xuất MP4 Video"** gọi API backend Python thực thi Remotion CLI + FFmpeg.
   - Bổ sung lệnh cheatcode **`@render-video [slug]`** và **`@preview-video [slug]`** để điều khiển trực tiếp qua chat.

3. **Quy tắc Auto-Sync trong Remotion Renderer**:
   - **Audio Narration**: Ghép các file `.wav` theo mốc thời gian chính xác từng frame (30fps) từ file timing Whisper.
   - **Phụ đề Karaoke**: Đổi màu từng chữ theo word timestamps (từ file `karaoke.srt` / `.ass`).
   - **Ảnh tĩnh (IMG)**: Tự động áp dụng hiệu ứng camera chuyển động mượt mà (Ken Burns: Zoom-in, Zoom-out, Pan trái/phải).
   - **Đồ họa chuyển động (GFX)**: Nạp các component từ bộ **20/20 Stack** (`ChartMotion`, `CounterNumber`, `CoinPhysics3D`...).
   - **Âm thanh nền (BGM)**: Hỗ trợ tự động hạ âm lượng (audio ducking) khi có giọng đọc narration.

4. **Kiến trúc Google Flow Đa Tài Khoản (Giai đoạn 2)**:
   - Sử dụng phương pháp **Chrome Remote Debugging Protocol (CDP)** với các user-data-dir riêng biệt (`profiles/acc1`, `acc2`...).
   - User đăng nhập Google tài khoản 1 lần, các phiên sau cookie/session tự động lưu vĩnh viễn.
   - Agent điều phối các sub-agent làm việc song song với từng cửa sổ Chrome qua port debug riêng (`9222`, `9223`, `9224`...).

5. **Chiến lược phân bổ Quota thông minh**:
   - **AIV (Video clip - tốn credit)**: Chia đều cho 5 account (mỗi account gánh 1-2 clip video để không vượt quota 50 credit/ngày, tổng cộng 250 credit/ngày).
   - **IMG (Ảnh tĩnh - 0 credit free)**: Bơm song song theo batch 3-4 prompt/lần để Google Flow xử lý nhanh nhất.
   - **Đồng bộ về local**: Tự động tải ảnh/video về đúng thư mục `channels/<channel>/videos/<slug>/assets/` và đổi tên đúng format chuẩn (`S001-A_6s_AIV.mp4`, `S002_IMG.png`).

---

## 🛠️ 3. Chi Tiết Triển Khai Giai Đoạn 1 (Remotion Video Studio)

### 3.1. Cấu trúc thư mục mới trong `studio/`:
```
studio/
├── app.py                       ← Thêm API render và API lấy video composition
├── templates/index.html         ← Thêm Tab "🎬 Video Preview & Timeline"
├── remotion/                    ← Remotion Video Project
│   ├── package.json             ← Remotion, @remotion/player, tailwind
│   ├── remotion.config.ts       ← Cấu hình fps, resolution 1080p, audio
│   ├── src/
│   │   ├── index.ts             ← Entry point
│   │   ├── Root.tsx             ← Khai báo Compositions
│   │   ├── VideoComposition.tsx ← Ghép chuỗi sequences theo timing
│   │   ├── components/
│   │   │   ├── KenBurnsImage.tsx
│   │   │   ├── KaraokeSubtitle.tsx
│   │   │   ├── VideoClipSequence.tsx
│   │   │   └── motion/          ← Chứa 20/20 motion components
│   │   └── types.ts
│   └── bundle/                  ← Bản build tĩnh nhúng vào Flask Web
```

### 3.2. Các API Backend trong `studio/app.py`:
- `GET /api/channels-videos`: Lấy danh sách channels và các video slug hiện có.
- `GET /api/video-data/<channel>/<slug>`: Lấy toàn bộ timeline data (composition JSON, danh sách audio wav, subtitle, assets).
- `POST /api/render-video`: Kích hoạt tiến trình `npx remotion render` ngầm và trả về tiến độ render (progress percentage).
- `GET /api/render-status/<task_id>`: Kiểm tra trạng thái render và cung cấp đường dẫn tải file `.mp4` hoàn tất.

### 3.3. Các Cheatcode Mới:
- `@render-video [slug]`: Kích hoạt render video tự động từ cửa sổ chat.
- `@preview-video [slug]`: Mở nhanh tab Studio Preview tới video đang làm việc.

---

## 🌐 4. Chi Tiết Thiết Kế Giai Đoạn 2 (Google Flow Multi-Account CDP Dispatcher)

- Thư mục công cụ: `tools/flow-dispatcher/`
- Thư mục lưu Chrome Profiles: `tools/flow-dispatcher/profiles/acc{1..5}`
- File cấu hình: `tools/flow-dispatcher/accounts.json`
- Lệnh điều khiển:
  - `@flow-login <acc_id>`: Bật Chrome cửa sổ riêng để user đăng nhập tài khoản Google.
  - `@flow-dispatch <slug>`: Agent tự động phân chia batch prompts cho 5 account và cào assets về local.
  - `@flow-status`: Xem trạng thái các account và số dư credit còn lại trong ngày.

---

## 🚀 5. Các Bước Thực Hiện Cụ Thể (Action Plan)

- [x] **Bước 0**: Lưu bản kế hoạch này vào repo và commit Git.
- [ ] **Bước 1**: Khởi tạo project Remotion bên trong `studio/remotion/` với các dependencies cần thiết.
- [ ] **Bước 2**: Xây dựng core components: `VideoComposition.tsx`, `KenBurnsImage.tsx`, `KaraokeSubtitle.tsx`.
- [ ] **Bước 3**: Cập nhật backend `studio/app.py` với các endpoints `/api/channels-videos`, `/api/video-data`, `/api/render-video`.
- [ ] **Bước 4**: Thêm Tab "🎬 Video Preview & Timeline" vào `studio/templates/index.html` nhúng Remotion Player.
- [ ] **Bước 5**: Thêm lệnh cheatcode `@render-video` và `@preview-video` vào Skill.
- [ ] **Bước 6**: Kiểm thử render thực tế trên video `thoat-bay-no-the-tin-dung` của kênh `tien-thuc-chien`.
