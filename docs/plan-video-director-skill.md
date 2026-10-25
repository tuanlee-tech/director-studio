# Chuyển đổi Gem2 Video Director → Antigravity Skill (Audio-First Workflow)

## Mô tả mục tiêu

Chuyển đổi tài liệu [gem2-video-director.md](file:///c:/Users/tuanlee/Downloads/files%20(1)/faceless-gem-notebooklm/faceless-gem-notebooklm/02-gems/gem2-video-director.md) — hiện dùng để chat thủ công với Gemini Gems — thành một **Antigravity skill** hoạt động trong agent harness. Skill sẽ hỗ trợ toàn bộ quy trình sản xuất video YouTube faceless với triết lý **audio-first**: tạo narration audio trước → đo timing chính xác → từ đó quyết định subtitle karaoke và số lượng B-roll tương ứng.

Repo `audio/` sẽ chứa nhiều channel, mỗi channel có thư mục riêng với channel-bible, videos và assets.

---

## User Review Required

> [!IMPORTANT]
> **Thay đổi triết lý quy trình**: Gem2 gốc tạo TTS text *song song* với prompt asset, scene duration cố định dựa trên đếm từ. Skill mới sẽ đảo quy trình: **audio narration → word-level timing → subtitle + B-roll planning**. Điều này thay đổi fundamentally cách xác định thời lượng scene.

> [!WARNING]
> **VieNeu-TTS API integration**: Skill sẽ tự động gọi VieNeu-TTS API (localhost:8000) khi service chạy, fallback sang manual khi không có. Cần xác nhận VieNeu-TTS API có hỗ trợ **word-level timestamps** không, hoặc cần dùng thêm công cụ alignment (forced alignment với Whisper hoặc tương tự).

---

## Decisions (Resolved)

> [!TIP]
> **Word-level timing — ĐÃ CHỐT: Whisper**
> Dùng Whisper (Python `openai-whisper` hoặc `whisper.cpp`) để transcribe lại audio → lấy word-level timestamps. Lý do:
> - Chạy đa nền tảng (Windows + Ubuntu)
> - Tận dụng GPU khi có (CUDA)
> - Độ chính xác cao nhất cho timeline
> - Fallback sang CPU khi không có GPU

> [!TIP]
> **B-roll planning — ĐÃ CHỐT: Auto + Review**
> - Agent **tự động** phân tích narration content và quyết định số lượng, thời lượng B-roll dựa trên Whisper timestamps
> - Hệ thống xuất **file JSON review** (`broll-plan.json`) + hiển thị dạng timeline/table để user **REVIEW và CHỈNH SỬA** trước khi tạo asset prompts
> - Chỉ sau khi user approve broll-plan mới tiến hành Phase 4 (Asset Prompts)

---

## Proposed Changes

### Cấu trúc tổng thể

```
audio/
├── .agents/
│   └── skills/
│       └── video-director/              ← Skill chính
│           ├── SKILL.md                 ← Entry point + hướng dẫn agent
│           ├── references/
│           │   ├── camera-vocabulary.md
│           │   ├── channel-bible.template.md
│           │   ├── shot-list.template.md
│           │   └── assembly-checklist.md
│           ├── scripts/
│           │   ├── tts-generate.ps1     ← Gọi VieNeu-TTS API tạo audio
│           │   ├── audio-analyze.py     ← Phân tích timing (word-level)
│           │   └── subtitle-gen.py      ← Sinh subtitle karaoke từ timing
│           └── resources/
│               └── tts-profiles.md      ← Cấu hình TTS profiles (gemini-3.8/3.1/vieneu)
├── channels/
│   └── <channel-name>/                  ← Mỗi kênh một thư mục
│       ├── channel-bible.md
│       ├── schedule.md                  ← Lịch trình video
│       └── videos/
│           └── <video-slug>/            ← Đặt tên thư mục theo slug của video (ví dụ: ai-thay-doi-giao-duc)
│               ├── script.md            ← Kịch bản theo scene
│               ├── audio/
│               │   ├── S001_narration.wav
│               │   ├── S001_timing.json ← Word-level timestamps
│               │   ├── S002_narration.wav
│               │   └── S002_timing.json
│               ├── assets/              ← Bỏ tiền tố video, chỉ giữ Scene ID
│               │   ├── S001_6s_AIV_sb.png
│               │   ├── S001_6s_AIV.mp4
│               │   └── S002_IMG.png
│               ├── subtitles/
│               │   └── karaoke.srt      ← Subtitle karaoke style
│               └── broll-plan.md        ← B-roll planning dựa trên timing
├── studio/
├── VieNeu-TTS/
└── ...
```

---

### Component 1: Skill Definition

#### [NEW] `.agents/skills/video-director/SKILL.md`

Entry point cho agent. Đây là file quan trọng nhất, chứa toàn bộ hướng dẫn quy trình.

```markdown
---
name: video-director
description: >-
  Skill tạo video YouTube faceless theo quy trình audio-first. Kích hoạt khi
  user muốn tạo video mới, quản lý lịch trình video, viết kịch bản, tạo TTS
  audio, phân tích timing, lên kế hoạch B-roll, sinh subtitle karaoke, và
  tạo prompt cho AI image/video. Hỗ trợ đa kênh (multi-channel).
---

# Video Director — Audio-First Faceless YouTube Production

## Tổng quan quy trình

Quy trình sản xuất video tuân theo triết lý **Audio-First**: giọng đọc (narration)
là trục chính, mọi thứ khác (hình ảnh, subtitle, hiệu ứng) đồng bộ theo timing
của audio.

### Pipeline

```mermaid
flowchart LR
  A["1. Kịch bản"] --> B["2. TTS Audio"]
  B --> C["3. Timing Analysis"]
  C --> D["4. Subtitle Karaoke"]
  C --> E["5. B-roll Planning"]
  E --> F["6. Asset Prompts"]
  F --> G["7. Assembly"]
```

## Phase 1 — Khởi tạo & Lịch trình
(Chi tiết quy trình từ gem2 gốc, được điều chỉnh cho agent...)

## Phase 2 — Kịch bản (Script)
(Viết script theo scene, đếm từ, tuân thủ ràng buộc thời lượng...)

## Phase 3 — Audio-First Pipeline ⭐ (KHÁC BIỆT CHÍNH)

### 3.1 Tạo TTS Audio cho từng scene
- Kiểm tra VieNeu-TTS service có đang chạy không (health check localhost:8000)
- Nếu có: tự động gọi API tạo audio cho từng scene
- Nếu không: xuất TTS text để user tự tạo, chờ user cung cấp audio files

### 3.2 Phân tích Timing
- Chạy script phân tích audio → word-level timestamps
- Output: JSON file cho mỗi scene chứa {word, start_ms, end_ms}

### 3.3 Xác định B-roll dựa trên Timing
- Phân tích nội dung narration → xác định "visual beats"
- Mỗi visual beat = 1 B-roll segment
- Duration B-roll = timing giữa các beats
- Ràng buộc AIV: chỉ 4/6/8/10s → snap duration về giá trị gần nhất

### 3.4 Sinh Subtitle Karaoke
- Từ word-level timing → subtitle .srt với highlight từng từ theo nhịp nói

## Phase 4 — Asset Prompts
(Prompt ảnh/video theo STYLE LOCK, camera vocabulary...)

## Phase 5 — Assembly Checklist
(Ráp video theo thứ tự...)
```

> [!NOTE]
> Nội dung chi tiết trong SKILL.md sẽ dài hơn nhiều. Ở trên chỉ là outline cấu trúc. Nội dung đầy đủ sẽ tích hợp toàn bộ logic từ gem2-video-director.md, được tái cấu trúc cho agent thay vì chat thủ công.

---

### Component 2: Channel Data Structure

#### [NEW] `channels/` directory structure

Mỗi channel là một thư mục con:

```
channels/<channel-name>/
├── channel-bible.md          ← Copy từ output Gem1, hoặc tạo mới
├── schedule.md               ← Lịch trình video (⬜/✅)
└── videos/
    └── <video-slug>/         ← Mỗi video một thư mục theo slug (ví dụ: ai-thay-doi-giao-duc)
        ├── script.md         ← Kịch bản chuẩn hóa
        ├── audio/            ← Narration audio + timing JSON
        ├── assets/           ← AI-generated images/videos (S001_6s_AIV.mp4, S002_IMG.png)
        ├── subtitles/        ← Subtitle karaoke (karaoke.srt)
        └── broll-plan.md     ← B-roll planning
```

Agent sẽ tự tạo cấu trúc này khi user nói "tạo channel mới" hoặc `@new-video <video-slug>`.

---

### Component 3: Reference Files

#### [NEW] `.agents/skills/video-director/references/camera-vocabulary.md`
Copy nguyên văn từ [camera-vocabulary.md](file:///c:/Users/tuanlee/Downloads/files%20(1)/faceless-gem-notebooklm/faceless-gem-notebooklm/03-knowledge/camera-vocabulary.md).

#### [NEW] `.agents/skills/video-director/references/channel-bible.template.md`
Copy nguyên văn từ [channel-bible.template.md](file:///c:/Users/tuanlee/Downloads/files%20(1)/faceless-gem-notebooklm/faceless-gem-notebooklm/03-knowledge/channel-bible.template.md).

#### [NEW] `.agents/skills/video-director/references/shot-list.template.md`
Copy nguyên văn từ [shot-list.template.md](file:///c:/Users/tuanlee/Downloads/files%20(1)/faceless-gem-notebooklm/faceless-gem-notebooklm/03-knowledge/shot-list.template.md).

#### [NEW] `.agents/skills/video-director/references/assembly-checklist.md`
Copy nguyên văn từ [assembly-checklist.md](file:///c:/Users/tuanlee/Downloads/files%20(1)/faceless-gem-notebooklm/faceless-gem-notebooklm/03-knowledge/assembly-checklist.md).

---

### Component 4: Automation Scripts

#### [NEW] `.agents/skills/video-director/scripts/tts-generate.ps1`

Script PowerShell gọi VieNeu-TTS API:

```powershell
# Tạo audio cho 1 scene
# Usage: .\tts-generate.ps1 -Text "Lời đọc scene" -Voice "ngoc-anh" -OutputPath "audio/S001.wav"

param(
    [Parameter(Mandatory)][string]$Text,
    [string]$Voice = "ngoc-anh",
    [string]$OutputPath,
    [string]$ApiUrl = "http://localhost:8000",
    [string]$Style = ""  # Cho gemini-3.8 style profile
)

# Health check
try {
    $health = Invoke-RestMethod "$ApiUrl/health" -TimeoutSec 5
} catch {
    Write-Error "VieNeu-TTS không chạy tại $ApiUrl. Hãy chạy 'launcher.ps1 start' trước."
    exit 1
}

# Gọi API
$body = @{
    model = "vieneu-tts-v3-turbo"
    input = $Text
    voice = $Voice
    response_format = "wav"
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "$ApiUrl/v1/audio/speech" `
    -Method POST -Body $body -ContentType "application/json" -TimeoutSec 120

[System.IO.File]::WriteAllBytes($OutputPath, $response.Content)
Write-Host "Audio saved: $OutputPath"
```

#### [NEW] `.agents/skills/video-director/scripts/audio-analyze.py`

Script Python phân tích audio timing (dùng Whisper hoặc tương tự):

```python
"""
Phân tích audio narration → word-level timestamps.
Usage: python audio-analyze.py <audio_file> <output_json>

Output JSON format:
{
  "duration_ms": 6320,
  "words": [
    {"word": "Mười", "start_ms": 120, "end_ms": 450},
    {"word": "lăm", "start_ms": 460, "end_ms": 680},
    ...
  ]
}
"""
import sys
import json

def analyze_with_whisper(audio_path: str) -> dict:
    """Dùng Whisper để transcribe + lấy word timestamps."""
    try:
        import whisper
        model = whisper.load_model("base")
        result = model.transcribe(audio_path, word_timestamps=True)
        words = []
        for segment in result["segments"]:
            for w in segment.get("words", []):
                words.append({
                    "word": w["word"].strip(),
                    "start_ms": int(w["start"] * 1000),
                    "end_ms": int(w["end"] * 1000),
                })
        # Lấy duration từ file
        import wave
        with wave.open(audio_path, 'r') as wf:
            duration_ms = int(wf.getnframes() / wf.getframerate() * 1000)
        return {"duration_ms": duration_ms, "words": words}
    except ImportError:
        return estimate_timing(audio_path)

def estimate_timing(audio_path: str) -> dict:
    """Fallback: ước lượng timing dựa trên PACE khi không có Whisper."""
    import wave
    with wave.open(audio_path, 'r') as wf:
        duration_ms = int(wf.getnframes() / wf.getframerate() * 1000)
    return {"duration_ms": duration_ms, "words": [], "note": "Install whisper for word-level timing"}

if __name__ == "__main__":
    audio_file = sys.argv[1]
    output_json = sys.argv[2]
    result = analyze_with_whisper(audio_file)
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"Timing saved: {output_json} ({result['duration_ms']}ms, {len(result['words'])} words)")
```

#### [NEW] `.agents/skills/video-director/scripts/subtitle-gen.py`

Script sinh subtitle karaoke từ timing data:

```python
"""
Sinh subtitle karaoke-style từ timing JSON.
Usage: python subtitle-gen.py <timing_dir> <output_srt>

Karaoke style: hiển thị nhóm 3-5 từ, highlight từ đang đọc.
"""
import sys
import json
import os
from pathlib import Path

def timing_to_karaoke_srt(timing_dir: str, output_srt: str):
    timing_files = sorted(Path(timing_dir).glob("*_timing.json"))
    srt_entries = []
    index = 1
    offset_ms = 0  # Offset tích lũy qua các scene

    for tf in timing_files:
        with open(tf, 'r', encoding='utf-8') as f:
            data = json.load(f)

        words = data.get("words", [])
        if not words:
            offset_ms += data.get("duration_ms", 0)
            continue

        # Nhóm từ (3-5 từ mỗi subtitle entry)
        group_size = 4
        for i in range(0, len(words), group_size):
            group = words[i:i + group_size]
            start = format_time(group[0]["start_ms"] + offset_ms)
            end = format_time(group[-1]["end_ms"] + offset_ms)
            text = " ".join(w["word"] for w in group)

            srt_entries.append(f"{index}\n{start} --> {end}\n{text}\n")
            index += 1

        offset_ms += data.get("duration_ms", 0)

    with open(output_srt, 'w', encoding='utf-8') as f:
        f.write("\n".join(srt_entries))
    print(f"Subtitle saved: {output_srt} ({index - 1} entries)")

def format_time(ms: int) -> str:
    h = ms // 3600000
    m = (ms % 3600000) // 60000
    s = (ms % 60000) // 1000
    ms_r = ms % 1000
    return f"{h:02d}:{m:02d}:{s:02d},{ms_r:03d}"

if __name__ == "__main__":
    timing_to_karaoke_srt(sys.argv[1], sys.argv[2])
```

---

### Component 5: TTS Profiles Resource

#### [NEW] `.agents/skills/video-director/resources/tts-profiles.md`

```markdown
# TTS Profiles

Cấu hình cho 3 engine TTS được hỗ trợ. Agent chọn profile dựa trên
CẤU HÌNH trong schedule.md của channel.

## gemini-3.8 (Mặc định)
- Không dùng tag ngoặc vuông
- Tag góc nhọn: <short pause> <long pause> <sigh> <laugh> <breath> <gasp>
- Cảm xúc/giọng điều khiển bằng STYLE (tiếng Anh, ≤ 8 từ)
- Chia khối TTS theo style, gom ít khối nhất

## gemini-3.1
- Tag ngoặc vuông tiếng Anh
- Cảm xúc: [neutral] [calm] [curious] [serious] [tension] [hope]
  [frustration] [amusement] [awe] [excited]
- Nhịp: [slow] [fast]
- Khoảng lặng: [short pause] [medium pause] [long pause]

## vieneu (VieNeu-TTS)
- 3 tag: [cười] [thở dài] [hắng giọng]
- Cảm xúc bằng câu ngắn, dấu phẩy, "...", "—"
- Mỗi câu ≤ 256 ký tự
- Gọi qua API localhost:8000
```

---

### Component 6: SKILL.md Chi tiết — Audio-First Pipeline

Phần quan trọng nhất trong SKILL.md là hướng dẫn agent thực hiện **Phase 3 (Audio-First)**. Dưới đây là logic chi tiết:

#### Luồng xử lý Audio-First

```mermaid
flowchart TD
    A["Script hoàn chỉnh<br>(scene list + narration text)"] --> B{"VieNeu-TTS<br>đang chạy?"}
    B -->|Có| C["Tự động gọi API<br>tạo .wav cho từng scene"]
    B -->|Không| D["Xuất TTS text<br>User tự tạo audio"]
    D --> E["User upload<br>audio files"]
    C --> F["Audio files<br>trong video/{slug}/audio/"]
    E --> F
    F --> G["Chạy audio-analyze.py<br>→ timing JSON"]
    G --> H["Phân tích visual beats<br>trong narration"]
    H --> I{"Từng visual beat"}
    I --> J["Tính duration<br>từ word timing"]
    J --> K["Snap to<br>4/6/8/10s"]
    K --> L["Gán loại<br>AIV / IMG / GFX"]
    L --> M["Tạo asset prompt<br>+ STYLE LOCK"]
    H --> N["Sinh subtitle<br>karaoke .srt"]
    M --> O["Bảng B-roll Plan"]
    N --> P["Output hoàn chỉnh"]
    O --> P
```

#### So sánh Gem2 gốc vs Skill mới

| Khía cạnh | Gem2 gốc | Skill mới (Audio-First) |
|---|---|---|
| Xác định duration scene | Đếm từ × PACE → ước lượng | TTS audio → đo thực tế |
| Số B-roll per scene | 1 scene = 1 asset (cố định) | 1 scene narration → N visual beats → N B-rolls |
| Subtitle | Không tạo tự động | Tự sinh karaoke .srt từ word timing |
| TTS | Xuất text, user tự tạo | Auto nếu có VieNeu-TTS, fallback manual |
| Quản lý file | Không | Cấu trúc thư mục chuẩn per-channel/per-video |
| Quy trình | Chat tuần tự | Agent-driven pipeline với scripts |

#### Logic xác định số B-roll cho 1 scene narration

```
Scene narration: "Năm 1969, con người lần đầu đặt chân lên Mặt Trăng.
                  Neil Armstrong bước ra khỏi tàu, nói câu nói nổi tiếng.
                  Hàng triệu người trên Trái Đất theo dõi qua truyền hình."

→ Visual beats phân tích:
  Beat 1: "Năm 1969... Mặt Trăng" → Cảnh tên lửa phóng / Mặt Trăng (6s AIV)
  Beat 2: "Neil Armstrong bước ra... nổi tiếng" → Phi hành gia bước xuống (4s AIV)
  Beat 3: "Hàng triệu người... truyền hình" → Đám đông xem TV (4s AIV)

→ Thay vì 1 clip 14s (không hợp lệ AIV), ta có 3 B-rolls tổng 14s
→ Mỗi B-roll duration snap vào {4,6,8,10}s dựa trên word timing thực tế
```

---

### Component 7: Cheatcode API Layer ⭐ (MỚI)

Lớp trừu tượng giữa user và hệ thống scripts. User gõ lệnh ngắn (cheatcode) trong
chat → agent nhận diện → detect OS → chạy script phù hợp bên dưới. Mục tiêu: user
không cần biết PowerShell/Bash, chỉ cần nhớ cheatcode.

#### Kiến trúc 3 tầng

```mermaid
flowchart TD
    U["User gõ: @gen-audio -t 'Xin chào'"] --> A["Agent nhận diện cheatcode<br>từ registry"]
    A --> D{"OS Detection"}
    D -->|Windows| W["Chạy scripts/*.ps1"]
    D -->|Linux/Mac| L["Chạy scripts/*.sh"]
    W --> R["Trả kết quả cho user"]
    L --> R
    
    C["config.json<br>(defaults: voice, channel...)"] -.-> A
    REG["cheatcodes.json<br>(registry)"] -.-> A
```

#### File mới cần tạo

| File | Mô tả |
|---|---|
| `resources/cheatcodes.json` | Registry: map cheatcode → script + params + help |
| `resources/config.json` | User defaults (voice, channel, pace, style...) |
| `scripts/tts-generate.sh` | Linux version của tts-generate.ps1 |
| `scripts/audio-analyze.sh` | Linux wrapper cho audio-analyze.py |
| `scripts/subtitle-gen.sh` | Linux wrapper cho subtitle-gen.py |
| `scripts/health-check.py` | Cross-platform health check (Python) |

#### Cheatcode Registry (`cheatcodes.json`)

```json
{
  "_meta": {
    "version": "1.0",
    "description": "Video Director Cheatcode Registry. Agent đọc file này để map user commands → scripts."
  },

  "🔧 CONFIG": {
    "@set-voice": {
      "description": "Set giọng đọc mặc định cho TTS",
      "usage": "@set-voice <voice-name>",
      "examples": ["@set-voice ngoc-anh", "@set-voice nam-minh"],
      "action": "update_config",
      "config_key": "default_voice",
      "available_values": ["ngoc-anh", "nam-minh", "thu-hien", "quang-anh", "lan-nhi", "duc-manh"]
    },
    "@set-channel": {
      "description": "Set channel đang làm việc",
      "usage": "@set-channel <channel-name>",
      "examples": ["@set-channel my-tech-channel"],
      "action": "update_config",
      "config_key": "active_channel"
    },
    "@set-pace": {
      "description": "Set tốc độ đọc mặc định (từ/giây)",
      "usage": "@set-pace <number>",
      "examples": ["@set-pace 4", "@set-pace 3.5"],
      "action": "update_config",
      "config_key": "default_pace"
    },
    "@set-tts": {
      "description": "Set TTS engine mặc định",
      "usage": "@set-tts <engine>",
      "examples": ["@set-tts vieneu", "@set-tts gemini-3.8"],
      "action": "update_config",
      "config_key": "tts_engine",
      "available_values": ["vieneu", "gemini-3.8", "gemini-3.1"]
    },
    "@set-style": {
      "description": "Set hoặc cập nhật STYLE LOCK descriptor",
      "usage": "@set-style <style text>",
      "examples": ["@set-style Cinematic dark moody..."],
      "action": "update_config",
      "config_key": "style_lock"
    },
    "@config": {
      "description": "Xem toàn bộ config hiện tại",
      "usage": "@config",
      "action": "read_config"
    }
  },

  "📁 PROJECT": {
    "@new-channel": {
      "description": "Tạo channel mới với cấu trúc thư mục chuẩn",
      "usage": "@new-channel <channel-name>",
      "examples": ["@new-channel ai-explained-vn"],
      "action": "create_directory_structure",
      "template": "channels/{name}/"
    },
    "@new-video": {
      "description": "Tạo video mới theo slug trong channel đang active",
      "usage": "@new-video <video-slug|tiêu đề>",
      "examples": ["@new-video ai-thay-doi-giao-duc", "@new-video \"AI thay đổi giáo dục\""],
      "action": "create_directory_structure",
      "template": "channels/{channel}/videos/{video-slug}/"
    },
    "@status": {
      "description": "Xem trạng thái tổng quan: channel, video, services",
      "usage": "@status",
      "action": "aggregate_status"
    },
    "@ls": {
      "description": "Liệt kê channels hoặc videos trong channel hiện tại",
      "usage": "@ls [channels|videos]",
      "examples": ["@ls channels", "@ls videos"]
    }
  },

  "🎙️ AUDIO": {
    "@gen-audio": {
      "description": "Tạo TTS audio cho 1 scene hoặc tất cả scenes",
      "usage": "@gen-audio -t \"text\" [-voice name] [-scene N] [--all]",
      "examples": [
        "@gen-audio -t \"Năm 1969, con người đặt chân lên Mặt Trăng\"",
        "@gen-audio -t \"Hello world\" -voice nam-minh",
        "@gen-audio --all",
        "@gen-audio -scene 3"
      ],
      "script": {
        "windows": "scripts/tts-generate.ps1",
        "linux": "scripts/tts-generate.sh"
      },
      "requires_service": "vieneu-tts",
      "fallback": "Xuất TTS text để user tự tạo"
    },
    "@gen-all-audio": {
      "description": "Tạo audio cho TẤT CẢ scenes trong video hiện tại",
      "usage": "@gen-all-audio [-voice name]",
      "examples": ["@gen-all-audio", "@gen-all-audio -voice thu-hien"],
      "action": "batch_tts",
      "requires_service": "vieneu-tts"
    },
    "@play": {
      "description": "Phát audio scene để preview",
      "usage": "@play <scene-number>",
      "examples": ["@play 3"],
      "action": "play_audio"
    }
  },

  "⏱️ TIMING": {
    "@analyze": {
      "description": "Phân tích timing audio (Whisper word-level timestamps)",
      "usage": "@analyze [-scene N] [--all]",
      "examples": ["@analyze -scene 3", "@analyze --all"],
      "script": "scripts/audio-analyze.py",
      "cross_platform": true
    },
    "@timing": {
      "description": "Xem timing analysis của scene hoặc toàn video",
      "usage": "@timing [-scene N] [--all]",
      "examples": ["@timing -scene 3", "@timing --all"],
      "action": "read_timing_json"
    }
  },

  "🎬 B-ROLL": {
    "@plan-broll": {
      "description": "Tự động lên kế hoạch B-roll từ timing data",
      "usage": "@plan-broll [--auto-approve]",
      "examples": ["@plan-broll"],
      "action": "generate_broll_plan",
      "output": "broll-plan.json"
    },
    "@show-broll": {
      "description": "Hiển thị B-roll plan dạng timeline table",
      "usage": "@show-broll",
      "action": "display_broll_plan"
    },
    "@edit-broll": {
      "description": "Chỉnh sửa B-roll plan (thêm/xóa/đổi duration)",
      "usage": "@edit-broll <scene> <action>",
      "examples": [
        "@edit-broll S003 split 2",
        "@edit-broll S003 merge S004",
        "@edit-broll S003 duration 6s",
        "@edit-broll S003 type IMG"
      ]
    },
    "@approve-broll": {
      "description": "Duyệt B-roll plan, cho phép chuyển sang Phase 4",
      "usage": "@approve-broll",
      "action": "lock_broll_plan"
    }
  },

  "📝 SUBTITLE": {
    "@gen-subs": {
      "description": "Sinh subtitle karaoke từ timing data",
      "usage": "@gen-subs [--format srt|ass|vtt]",
      "examples": ["@gen-subs", "@gen-subs --format ass"],
      "script": "scripts/subtitle-gen.py",
      "cross_platform": true
    },
    "@preview-subs": {
      "description": "Xem preview subtitle với word highlighting",
      "usage": "@preview-subs [-scene N]",
      "action": "display_subtitle_preview"
    }
  },

  "🎨 ASSETS": {
    "@gen-prompts": {
      "description": "Tạo asset prompts (ảnh/video) từ B-roll plan đã duyệt",
      "usage": "@gen-prompts [-scene N] [--all]",
      "examples": ["@gen-prompts --all", "@gen-prompts -scene 3"],
      "action": "generate_asset_prompts",
      "requires": "approved_broll_plan"
    },
    "@show-prompts": {
      "description": "Hiển thị bảng prompts đã tạo",
      "usage": "@show-prompts",
      "action": "display_prompt_table"
    },
    "@shot-list": {
      "description": "Xuất shot list đầy đủ cho video",
      "usage": "@shot-list [--export md|json]",
      "action": "export_shot_list"
    }
  },

  "📋 SCRIPT": {
    "@gen-script": {
      "description": "Tạo kịch bản video từ chủ đề/outline",
      "usage": "@gen-script \"<topic>\" [-minutes N]",
      "examples": ["@gen-script \"AI thay đổi giáo dục\" -minutes 8"],
      "action": "generate_script"
    },
    "@show-script": {
      "description": "Hiển thị kịch bản hiện tại",
      "usage": "@show-script [-scene N]",
      "action": "display_script"
    },
    "@edit-scene": {
      "description": "Sửa nội dung 1 scene trong kịch bản",
      "usage": "@edit-scene <N> \"<new text>\"",
      "examples": ["@edit-scene 3 \"Nội dung mới cho scene 3\""],
      "action": "edit_scene_in_script"
    }
  },

  "📅 SCHEDULE": {
    "@schedule": {
      "description": "Xem/quản lý lịch trình video",
      "usage": "@schedule [show|add|done N]",
      "examples": [
        "@schedule show",
        "@schedule add \"Tiêu đề video mới\"",
        "@schedule done 3"
      ]
    }
  },

  "🏥 HEALTH": {
    "@health": {
      "description": "Kiểm tra trạng thái tất cả services (TTS, Studio, Whisper...)",
      "usage": "@health",
      "script": "scripts/health-check.py",
      "cross_platform": true
    },
    "@start-tts": {
      "description": "Khởi động VieNeu-TTS service",
      "usage": "@start-tts",
      "script": {
        "windows": "../../launcher.ps1 start",
        "linux": "../../launcher.sh start"
      }
    },
    "@stop-tts": {
      "description": "Dừng VieNeu-TTS service",
      "usage": "@stop-tts",
      "script": {
        "windows": "../../launcher.ps1 stop",
        "linux": "../../launcher.sh stop"
      }
    }
  },

  "🔄 PIPELINE": {
    "@pipeline": {
      "description": "Chạy toàn bộ pipeline cho video hiện tại (hoặc từ step chỉ định)",
      "usage": "@pipeline [--from step]",
      "examples": [
        "@pipeline",
        "@pipeline --from audio",
        "@pipeline --from broll"
      ],
      "action": "run_full_pipeline",
      "steps": ["script", "audio", "analyze", "broll", "prompts", "subs"]
    },
    "@next": {
      "description": "Chuyển sang bước tiếp theo trong pipeline",
      "usage": "@next",
      "action": "advance_pipeline"
    },
    "@undo": {
      "description": "Quay lại bước trước trong pipeline",
      "usage": "@undo",
      "action": "revert_pipeline_step"
    }
  },

  "❓ HELP": {
    "@help": {
      "description": "Hiển thị danh sách tất cả cheatcodes",
      "usage": "@help [category|command]",
      "examples": ["@help", "@help audio", "@help @gen-audio"]
    },
    "@cheatsheet": {
      "description": "Hiển thị bảng tóm tắt cheatcodes (1 trang)",
      "usage": "@cheatsheet"
    }
  }
}
```

#### Config File (`config.json`)

Lưu tại `channels/<channel>/config.json`, agent đọc/ghi khi user dùng `@set-*`:

```json
{
  "active_channel": "my-channel",
  "active_video": "ai-thay-doi-giao-duc",
  "default_voice": "ngoc-anh",
  "default_pace": 4,
  "tts_engine": "vieneu",
  "tts_api_url": "http://localhost:8000",
  "whisper_model": "base",
  "style_lock": "",
  "language": "vi",
  "video_duration_target_minutes": 8,
  "static_image_exempt": true,
  "subtitle_format": "srt",
  "subtitle_group_size": 4
}
```

#### Agent OS Detection Logic

Trong SKILL.md, agent được hướng dẫn:

```markdown
## OS Detection & Script Dispatch

Khi user gõ cheatcode, agent thực hiện:

1. **Detect OS**: Kiểm tra biến môi trường hoặc chạy `python -c "import platform; print(platform.system())"`
2. **Lookup registry**: Đọc `cheatcodes.json` → tìm entry matching
3. **Resolve defaults**: Merge params user truyền vào với `config.json`
4. **Dispatch**:
   - `action` type → agent tự thực hiện (tạo file, đọc file, phân tích...)
   - `script` type → chạy script tương ứng với OS:
     - Windows → `.ps1` via PowerShell
     - Linux/Mac → `.sh` via Bash
   - `cross_platform: true` → script Python, chạy trực tiếp
5. **Report**: Trả kết quả cho user dạng dễ đọc
```

#### Cross-platform Script Example

Mỗi script OS-specific sẽ có cặp `.ps1` / `.sh`:

**`scripts/tts-generate.sh`** (Linux counterpart):
```bash
#!/bin/bash
# Usage: ./tts-generate.sh -t "Lời đọc" -voice "ngoc-anh" -o "audio/S001.wav"

TEXT="" VOICE="ngoc-anh" OUTPUT="" API="http://localhost:8000"

while [[ $# -gt 0 ]]; do
  case $1 in
    -t|--text)  TEXT="$2"; shift 2 ;;
    -voice)     VOICE="$2"; shift 2 ;;
    -o|--output) OUTPUT="$2"; shift 2 ;;
    -api)       API="$2"; shift 2 ;;
    *)          shift ;;
  esac
done

# Health check
if ! curl -sf "$API/health" > /dev/null 2>&1; then
  echo "ERROR: VieNeu-TTS không chạy tại $API" >&2; exit 1
fi

# Gọi API
curl -sf -X POST "$API/v1/audio/speech" \
  -H "Content-Type: application/json" \
  -d "{\"model\":\"vieneu-tts-v3-turbo\",\"input\":\"$TEXT\",\"voice\":\"$VOICE\",\"response_format\":\"wav\"}" \
  -o "$OUTPUT"

echo "Audio saved: $OUTPUT"
```

#### Bảng tóm tắt Cheatcodes (cho @cheatsheet)

| Category | Cheatcode | Mô tả ngắn |
|---|---|---|
| **🔧 Config** | `@set-voice` | Đổi giọng mặc định |
| | `@set-channel` | Chọn channel đang làm |
| | `@set-pace` | Set tốc độ đọc |
| | `@set-tts` | Đổi TTS engine |
| | `@set-style` | Set STYLE LOCK |
| | `@config` | Xem toàn bộ config |
| **📁 Project** | `@new-channel` | Tạo channel mới |
| | `@new-video` | Tạo video mới |
| | `@status` | Trạng thái tổng quan |
| | `@ls` | Liệt kê channels/videos |
| **🎙️ Audio** | `@gen-audio` | Tạo audio 1 scene |
| | `@gen-all-audio` | Tạo audio mọi scene |
| | `@play` | Phát preview audio |
| **⏱️ Timing** | `@analyze` | Chạy Whisper phân tích |
| | `@timing` | Xem timing data |
| **🎬 B-roll** | `@plan-broll` | Auto lên kế hoạch B-roll |
| | `@show-broll` | Xem B-roll plan |
| | `@edit-broll` | Sửa B-roll plan |
| | `@approve-broll` | Duyệt B-roll → Phase 4 |
| **📝 Subtitle** | `@gen-subs` | Sinh subtitle karaoke |
| | `@preview-subs` | Preview subtitle |
| **🎨 Assets** | `@gen-prompts` | Tạo prompts từ B-roll plan |
| | `@show-prompts` | Xem bảng prompts |
| | `@shot-list` | Xuất shot list |
| **📋 Script** | `@gen-script` | Tạo kịch bản |
| | `@show-script` | Xem kịch bản |
| | `@edit-scene` | Sửa 1 scene |
| **📅 Schedule** | `@schedule` | Quản lý lịch trình |
| **🏥 Health** | `@health` | Check services |
| | `@start-tts` | Bật TTS service |
| | `@stop-tts` | Tắt TTS service |
| **🔄 Pipeline** | `@pipeline` | Chạy toàn bộ pipeline |
| | `@next` | Bước tiếp theo |
| | `@undo` | Quay lại bước trước |
| **❓ Help** | `@help` | Xem chi tiết lệnh |
| | `@cheatsheet` | Bảng tóm tắt |

---

## Verification Plan

### Automated Tests

```powershell
# 1. Kiểm tra cấu trúc skill hợp lệ
Test-Path "c:\Users\tuanlee\Downloads\audio\.agents\skills\video-director\SKILL.md"

# 2. Kiểm tra scripts chạy được
python "c:\Users\tuanlee\Downloads\audio\.agents\skills\video-director\scripts\audio-analyze.py" --help
python "c:\Users\tuanlee\Downloads\audio\.agents\skills\video-director\scripts\subtitle-gen.py" --help

# 3. Kiểm tra reference files tồn tại
Get-ChildItem "c:\Users\tuanlee\Downloads\audio\.agents\skills\video-director\references\"

# 4. Test tạo channel structure
# (Agent tự tạo khi user gõ "tạo channel test-channel")
Test-Path "c:\Users\tuanlee\Downloads\audio\channels\"
```

### Manual Verification

1. **Skill discovery**: Mở Antigravity trong workspace `audio/`, kiểm tra skill `video-director` xuất hiện trong danh sách skills
2. **Channel creation**: Gõ "tạo channel test-channel" → kiểm tra thư mục được tạo đúng cấu trúc
3. **TTS integration**: Nếu VieNeu-TTS đang chạy, test auto-generate audio cho 1 scene ngắn
4. **Timing analysis**: Cung cấp file audio mẫu, kiểm tra output timing JSON
5. **Subtitle generation**: Từ timing JSON, kiểm tra file .srt output
6. **End-to-end**: Chạy thử toàn bộ quy trình cho 1 video 3-scene ngắn

---

## Danh sách file sẽ tạo

| # | File | Mô tả |
|---|---|---|
| 1 | `.agents/skills/video-director/SKILL.md` | Entry point skill — toàn bộ hướng dẫn quy trình |
| 2 | `.agents/skills/video-director/references/camera-vocabulary.md` | Camera vocabulary reference |
| 3 | `.agents/skills/video-director/references/channel-bible.template.md` | Channel Bible template |
| 4 | `.agents/skills/video-director/references/shot-list.template.md` | Shot list template |
| 5 | `.agents/skills/video-director/references/assembly-checklist.md` | Assembly checklist |
| 6 | `.agents/skills/video-director/scripts/tts-generate.ps1` | TTS API caller script |
| 7 | `.agents/skills/video-director/scripts/audio-analyze.py` | Audio timing analyzer |
| 8 | `.agents/skills/video-director/scripts/subtitle-gen.py` | Subtitle karaoke generator |
| 9 | `.agents/skills/video-director/resources/tts-profiles.md` | TTS engine profiles |
| 10 | `channels/.gitkeep` | Placeholder cho channels directory |
