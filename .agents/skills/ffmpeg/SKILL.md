---
name: ffmpeg
description: >-
  Kỹ năng FFmpeg chuyên sâu: Ghép nối audio narration master, mux đa luồng âm thanh BGM & voice,
  chuẩn hóa âm lượng EBU R128 (-14 LUFS), hardware acceleration NVENC/QSV, và xuất video MP4 chất lượng cao.
---

# 🎞️ FFmpeg — Xử Lý Media & Xuất Bản Video Đỉnh Cao

FFmpeg là tiêu chuẩn vàng xử lý đa phương tiện thế giới. Trong quy trình Audio-First Video Pipeline, FFmpeg đảm nhận các trọng trách then chốt về âm thanh master và xuất file MP4 cuối cùng.

## 🎯 Ứng Dụng Sống Còn Trong Dự Án

### 1. Ghép Nối Audio Narration Master (Tránh Lỗi CLI Overflow Trên Windows)
Khi kịch bản có hàng chục cảnh (S001 -> S040), việc truyền danh sách file dài hàng nghìn ký tự vào Windows CLI sẽ gây lỗi tràn bộ nhớ đệm lệnh. Giải pháp chuẩn là dùng concat file list:
```bash
# file_list.txt
file 'S001.mp3'
file 'S002.mp3'
...
ffmpeg -y -f concat -safe 0 -i file_list.txt -c copy master_narration.mp3
```

### 2. Chuẩn Hóa Âm Lượng YouTube (EBU R128 Loudness Normalization)
Đảm bảo âm thanh đạt tiêu chuẩn -14 LUFS, không bị YouTube giảm âm lượng hoặc khán giả phải tự điều chỉnh âm lượng:
```bash
ffmpeg -i input.mp3 -af loudnorm=I=-14:LRA=7:tp=-1.5 output_normalized.mp3
```

### 3. Hòa Âm Narration Master và BGM (Sidechain / Ducking)
Tự động dìm BGM khi có giọng đọc narration:
```bash
ffmpeg -i voice.mp3 -i bgm.mp3 -filter_complex "[1:a]volume=0.18[bgm];[0:a][bgm]amix=inputs=2:duration=first" -c:a aac -b:a 192k final_audio.aac
```

### 4. Encode H.264 Video Chất Lượng Cao
```bash
ffmpeg -i raw_video.mp4 -i final_audio.aac -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -c:a copy -movflags +faststart final_video.mp4
```
- `-crf 18`: Đạt chuẩn chất lượng thị giác gần như không mất dữ liệu (Visually Lossless).
- `-movflags +faststart`: Đưa metadata Moov Atom lên đầu file để video phát ngay lập tức trên web/YouTube mà không cần tải hết file.
