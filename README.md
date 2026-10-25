# 🎛️ AI Audio & Video Platform — Monorepo

Hệ thống nền tảng sản xuất Video & Âm thanh AI đa dịch vụ:
- **VieNeu-TTS**: Vietnamese TTS & Voice Cloning (Port 7860)
- **Remotion Engine**: Hậu kỳ dựng video tự động, Motion Graphics 20/20 & Subtitle Karaoke (Port 3000)
- **Google Flow Multi-Account CDP Dispatcher**: Điều phối 5 tài khoản Chrome độc lập, tận dụng 250 credit video/ngày và cào ảnh 0 credit song song (Ports 9223-9227)

Hỗ trợ **100% cả Windows và Ubuntu / Linux**, chạy trực tiếp qua **1 lệnh duy nhất** (`python run.py`).

---

## ⚡ KHỞI ĐỘNG NHANH TOÀN DỰ ÁN (1 LỆNH DUY NHẤT)

Áp dụng cho cả **Ubuntu (Linux)** và **Windows**:

```bash
# Khởi động toàn bộ cụm dịch vụ (TTS + Studio UI + Flow CDP):
python run.py          # Trên Windows
python3 run.py         # Trên Ubuntu / Linux

# Xem bảng trạng thái realtime các cổng (7860, 3000, 9223-9227):
python run.py --status

# Dừng an toàn toàn bộ các dịch vụ:
python run.py --stop
```

> **Sau khi khởi động:**
> - 🎬 **Studio UI & Video Preview**: [http://localhost:3000](http://localhost:3000)
> - 🎙️ **VieNeu-TTS Voice Studio**: [http://localhost:7860](http://localhost:7860)
> - 🌐 **Google Flow Multi-Account**: Tab trên Web Studio (Ports 9223-9227)

---

## 🐧 Hướng dẫn thiết lập trên Ubuntu / Debian

### 1. Cài đặt các gói phụ thuộc trên Ubuntu (1 lần duy nhất)
```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip curl

# Nếu dùng tính năng xuất video Remotion (Node.js & npm):
sudo apt install -y nodejs npm

# Nếu dùng tính năng tự động cào Google Flow qua Chrome CDP trên Ubuntu:
sudo apt install -y chromium-browser
# hoặc tải Google Chrome chính thức:
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb || sudo apt -f install -y
```

### 2. Khởi chạy dự án trên Ubuntu
```bash
cd audio

# Cách 1 (Khuyên dùng): Dùng unified runner đa nền tảng
python3 run.py

# Cách 2: Dùng bash launcher
./launcher.sh start

# Cách 3: Dùng Docker Compose
docker compose --profile cpu up -d --build
```

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
