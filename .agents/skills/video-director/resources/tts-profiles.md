# TTS Profiles

Cấu hình cho các engine TTS được hỗ trợ. Agent chọn profile dựa trên
`tts_engine` trong file `config.json` của channel.

## vieneu (VieNeu-TTS) — ⭐ MẶC ĐỊNH

Engine mặc định. Chạy qua API localhost:8000 (OpenAI-compatible).

- **Default voice**: `Hải Đăng` (nếu đã enroll trong container), fallback → `Binh`
- **Built-in presets có sẵn**:
  | Key | Mô tả |
  |---|---|
  | `Hải Đăng` | Giọng đọc faceless (enroll trong container) |
  | `Binh` | Bình (nam miền Bắc) |
  | `Tuyen` | Tuyên (nam miền Bắc) |
  | `Vinh` | Vĩnh (nam miền Nam) |
  | `Doan` | Đoan (nữ miền Nam) |
  | `Ly` | Ly (nữ miền Bắc) |
  | `Ngoc` | Ngọc (nữ miền Bắc) |
- **Tags hỗ trợ**: `[cười]` `[thở dài]` `[hắng giọng]` — dùng tiết kiệm
- **Cảm xúc**: Dùng câu ngắn, dấu phẩy, `...`, `—` để gợi cảm xúc
- **Giới hạn**: Mỗi câu ≤ 256 ký tự

## gemini-3.8

- Không dùng tag ngoặc vuông `[...]`
- Tags cho sự kiện tức thời (góc nhọn): `<short pause>` `<long pause>` `<sigh>` `<laugh>` `<breath>` `<gasp>`
- Cảm xúc/giọng điều khiển bằng **STYLE** (tiếng Anh, ≤ 8 từ), đặt trên mỗi khối TTS
- Gom ít khối nhất: nhóm các cảnh liền nhau cùng cảm xúc thành 1 khối

## gemini-3.1

- Tags ngoặc vuông, tiếng Anh
- **Cảm xúc**: `[neutral]` `[calm]` `[curious]` `[serious]` `[tension]` `[hope]` `[frustration]` `[amusement]` `[awe]` `[excited]`
- **Nhịp**: `[slow]` `[fast]`
- **Khoảng lặng**: `[short pause]` ≈0.25s · `[medium pause]` ≈0.5s · `[long pause]` ≥1s
- Đặt pause giữa câu/ý, không cuối đoạn. `[long pause]` tối đa 1 lần mỗi 3 cảnh
