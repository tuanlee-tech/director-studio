# 🎛️ AI Audio Platform — Monorepo

Hệ thống nền tảng xử lý âm thanh AI đa dịch vụ (Text-to-Speech, Voice Cloning, Audio Processing...).  
Thiết kế theo mô hình **Monorepo**, hỗ trợ cả **Native (Python/uv)** và **Docker Compose**, tự động phát hiện phần cứng và graceful fallback giữa Windows và Ubuntu.

---

## 📌 Tổng quan kiến trúc (Architecture)

```
audio/                               ← Thư mục gốc Monorepo
├── launcher.ps1                     ← Smart Launcher cho Windows (PowerShell 5.1+)
├── launcher.sh                      ← Smart Launcher cho Linux/Ubuntu (Bash)
├── docker-compose.yml               ← Đóng gói toàn cụm (hỗ trợ profiles cpu / gpu)
├── .env.example                     ← File mẫu cấu hình biến môi trường
├── VieNeu-TTS/                      ← Service 1: Vietnamese TTS & Voice Cloning
│   ├── .venv/                       ← Virtual environment Python (uv managed)
│   ├── apps/
│   │   ├── gradio_main.py           ← Web UI chính (Gradio port 7860)
│   │   └── openai_speech.py         ← OpenAI-compatible API (port 8000)
│   ├── docker/
│   │   ├── Dockerfile.cpu           ← Image CPU nhẹ (ONNX Runtime, torch-free)
│   │   └── Dockerfile.gpu           ← Image GPU (PyTorch + CUDA 12.8)
│   └── src/                         ← Engine cốt lõi
└── studio/                          ← Service 2: UI Studio quản lý toàn bộ hệ thống
    ├── venv/                        ← Virtual environment Studio (Flask)
    ├── app.py                       ← Backend API & health check
    ├── templates/index.html         ← Giao diện Dashboard Dark-theme
    └── Dockerfile                   ← Dockerfile cho Studio container
```

---

## 🚀 Hướng dẫn nhanh theo từng môi trường

### 1. Máy Windows (Ví dụ: Windows 10 IoT LTSC / Win 10 / Win 11)

> **Lưu ý:** Trên các bản Windows không cài được Docker Desktop (như Windows 10 IoT LTSC), hệ thống sẽ chạy chế độ **Native-first** trực tiếp qua Python/uv cực kỳ mượt mà.

Mở PowerShell tại thư mục `c:\Users\tuanlee\Downloads\audio`:

```powershell
# Bước 1 (Lần đầu): Cài đặt tự động môi trường và thư viện
.\launcher.ps1 install

# Bước 2: Khởi chạy tất cả dịch vụ
.\launcher.ps1 start

# Bước 3: Kiểm tra trạng thái
.\launcher.ps1 status

# Dừng tất cả dịch vụ khi không dùng
.\launcher.ps1 stop
```

---

### 2. Máy Ubuntu (Không có GPU hoặc có GPU)

Hệ thống hỗ trợ 2 cách chạy trên Ubuntu:

#### Cách 2.1: Chạy Native (Khuyên dùng khi không muốn cài Docker)
```bash
cd ~/audio
chmod +x launcher.sh

# 1. Cài đặt tự động uv, venv và dependencies
./launcher.sh install

# 2. Khởi chạy (tự nhận diện không có GPU -> fallback sang ONNX CPU fp32)
./launcher.sh start

# Kiểm tra trạng thái & Dừng
./launcher.sh status
./launcher.sh stop
./launcher.sh restart
```

#### Cách 2.2: Chạy qua Docker Compose (Chuẩn đóng gói cụm container)
```bash
# Trường hợp máy KHÔNG có GPU (CPU Mode - siêu nhẹ, torch-free):
docker compose --profile cpu up -d --build

# Trường hợp máy CÓ NVIDIA GPU + NVIDIA Container Toolkit:
docker compose --profile gpu up -d --build

# Xem logs toàn cụm:
docker compose logs -f

# Dừng cụm:
docker compose down
```

---

## 🔄 Cơ chế Auto-detect & Graceful Fallback

Hệ thống launcher tự động kiểm tra phần cứng khi khởi động:

```
Kiểm tra NVIDIA GPU + VRAM
    │
    ├── Có GPU NVIDIA (≥ 6GB VRAM) + PyTorch CUDA ──> Chạy PyTorch Backend (Tăng tốc tối đa)
    │
    └── Không có GPU / VRAM nhỏ / Máy CPU thuần  ──> Graceful Fallback: ONNX Runtime CPU fp32
```

| Môi trường | Phần cứng | Backend hoạt động | Mô tả |
|------------|-----------|-------------------|-------|
| **Windows hiện tại** | GTX 1050 Ti (4GB) | `onnx-cpu` (fp32) | Chạy native cực ổn định, chất lượng giọng cao nhất |
| **Ubuntu Server** | Không có GPU (CPU) | `onnx-cpu` (fp32) | Tự động chọn ONNX runtime torch-free, tiêu tốn ít RAM |
| **Ubuntu Server** | Có GPU NVIDIA | `pytorch-cuda` | Kích hoạt tăng tốc sinh giọng qua CUDA |

---

## 🌐 Các cổng dịch vụ (Ports & Endpoints)

| Dịch vụ | URL / Port | Vai trò |
|---------|------------|---------|
| **🎛️ Studio Dashboard** | [http://localhost:3000](http://localhost:3000) | Giao diện trung tâm giám sát tình trạng hệ thống, cấu hình phần cứng, test nhanh giọng đọc |
| **🎙️ VieNeu TTS Web UI** | [http://localhost:7860](http://localhost:7860) | Giao diện Gradio đầy đủ tính năng: Clone giọng từ file mẫu, đọc văn bản, chọn preset giọng |
| **🔌 VieNeu Speech API** | [http://localhost:8000](http://localhost:8000) | Endpoint chuẩn tương thích OpenAI `/v1/audio/speech` |

---

## 🧩 Cách mở rộng & Thêm Service mới vào Monorepo

Monorepo được thiết kế mở để dễ dàng tích hợp thêm các mảnh ghép AI Audio khác (như STT Whisper, RVC Voice Conversion, MusicGen...):

1. **Tạo thư mục repo con**:
   ```
   audio/
   ├── VieNeu-TTS/
   ├── studio/
   └── whisper-stt/          ← Thêm repo mới vào đây
       ├── Dockerfile
       └── ...
   ```
2. **Khai báo vào [`docker-compose.yml`](file:///c:/Users/tuanlee/Downloads/audio/docker-compose.yml)**: Thêm service `whisper-stt` vào compose file với profile tương ứng (`cpu`/`gpu`).
3. **Đăng ký vào [`studio/app.py`](file:///c:/Users/tuanlee/Downloads/audio/studio/app.py)**: Thêm định nghĩa vào dictionary `SERVICES`:
   ```python
   SERVICES["whisper-stt"] = {
       "name": "Whisper STT",
       "description": "Speech-to-Text transcription",
       "icon": "📝",
       "port": 8001,
       "url": "http://localhost:8001",
       "health_endpoint": "/health"
   }
   ```
4. Studio UI sẽ tự động nhận diện service mới, hiển thị card giám sát và nút truy cập.

---

## 🛠️ Xử lý sự cố (Troubleshooting)

- **Lỗi `NamedParameterNotFound 'Environment'` trên Windows**:
  - Đã được xử lý: Script sử dụng gán biến môi trường `$env:...` trực tiếp, đảm bảo tương thích 100% với PowerShell 5.1 tích hợp sẵn của Windows 10/11.
- **Lỗi `UnicodeEncodeError` console Windows**:
  - Đã tích hợp tự động reconfigure `sys.stdout` sang `utf-8` trong `studio/app.py`.
- **Giao diện TTS không có model / Tải lỗi**:
  - Model `pnnbao-ump/VieNeu-TTS-v3-Turbo` (~521 MB) được cache tại thư mục HuggingFace (`~/.cache/huggingface`).
  - Lần khởi động đầu tiên máy sẽ tự động tải các file graph ONNX về máy; từ lần thứ 2 trở đi hệ thống đọc trực tiếp từ cache offline không cần tải lại.
