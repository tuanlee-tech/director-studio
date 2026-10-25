# SHOT LIST (mẫu)

Gem 2 xuất shot list ở bước S6 theo đúng định dạng này. Mỗi cảnh một khối để bạn copy prompt dễ dàng.

```
# SHOT LIST — <tên video>
Ngôn ngữ: <...> | Mục tiêu: <...> phút | Tổng thời lượng AI video: <...>s | Số cảnh: <...>
```

## Quy ước
- Loại cảnh: AIV (AI video), IMG (ảnh tĩnh), GFX (đồ họa chuyển động).
- Cảnh AIV: Dur chỉ được là 4, 6, 8 hoặc 10 giây. Số từ ≤ trần (4s → 12, 6s → 18, 8s → 24, 10s → 29 từ tiếng Việt).
- Tên file: `S{##}_{dur}s_{loại}.{đuôi}`, ví dụ `S07_6s_AIV.mp4`, `S08_IMG.png`.
- Mọi prompt ảnh/video chứa nguyên văn STYLE DESCRIPTOR và tuân NEGATIVE LIST trong Channel Bible.

## Khối cảnh

```
### S07 · 6s · AIV · file: S07_6s_AIV.mp4
- Beat: <tên beat>
- Lời đọc (16/18 từ): "<câu thoại>"
- Cỡ cảnh / góc máy / chuyển động: <ví dụ: MCU, thấp, push-in chậm>
- Prompt ảnh (khung đầu): <EN, có STYLE DESCRIPTOR>
- Prompt video: <EN, có STYLE DESCRIPTOR, mô tả chuyển động trong đúng 6s>
- Âm thanh / SFX: <...>
- Cắt sang cảnh sau: <hard cut | match cut | whip | dissolve ...> — tại cuối câu
```

```
### S08 · IMG · file: S08_IMG.png
- Beat: <tên beat>
- Lời đọc (24 từ): "<câu thoại>"
- Chuyển động áp bằng phần mềm: <zoom chậm | pan | tĩnh>
- Prompt ảnh: <EN, có STYLE DESCRIPTOR>
- Âm thanh / SFX: <...>
- Cắt sang cảnh sau: <...>
```
