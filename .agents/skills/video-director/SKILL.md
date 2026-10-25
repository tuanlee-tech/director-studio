---
name: video-director
description: >-
  Skill sản xuất video YouTube faceless theo quy trình Audio-First. Kích hoạt
  khi user muốn tạo video mới, quản lý lịch trình, viết kịch bản, tạo TTS audio
  tự động, phân tích timing bằng Whisper, lên kế hoạch B-roll, sinh subtitle
  karaoke, và tạo prompt AI image/video. Hỗ trợ đa kênh (multi-channel) và
  cheatcode API cho user không quen terminal.
---

# Video Director — Audio-First Faceless YouTube Production

## Triết lý cốt lõi

Giọng đọc (narration) là **trục chính**. Tạo audio trước → đo timing thực tế bằng
Whisper → từ đó quyết định chính xác: subtitle karaoke, số lượng B-roll và thời
lượng mỗi B-roll. Đảo ngược hoàn toàn so với quy trình truyền thống.

**Nguyên tắc bất biến:**
- Cảnh AI video (AIV) chỉ có đúng 4s / 6s / 8s / 10s. Không bao giờ dùng số giây khác.
- Không lặp clip, không kéo giãn clip.
- Cắt cảnh đúng cuối câu.
- Mọi prompt ảnh/video phải chứa nguyên văn STYLE LOCK từ Channel Bible.

---

## Cheatcode API — Cách tương tác

User gõ `@command` trong chat thay vì chạy lệnh terminal. Agent đọc `resources/cheatcodes.json`
để tra cứu và thực thi.

**Khi nhận cheatcode, agent:**
1. Lookup entry trong `resources/cheatcodes.json`
2. Detect OS: chạy `python -c "import platform; print(platform.system())"` → `Windows` hoặc `Linux`
3. Resolve defaults từ `channels/<active_channel>/config.json`
4. Dispatch:
   - `action` type → agent tự thực hiện (đọc/ghi file, phân tích, hiển thị)
   - `script.windows` → chạy `.ps1` via PowerShell
   - `script.linux` → chạy `.sh` via Bash
   - `cross_platform: true` → chạy `.py` via Python trực tiếp
5. Report kết quả cho user

**Gõ `@cheatsheet` để xem danh sách đầy đủ.**

---

## Quy tắc chung (KHÔNG hiển thị cho user, tự áp dụng)

- Không hỏi lại, không xin "ok", không khen, không rào đón.
- Thiếu thông tin → lấy từ Channel Bible hoặc dùng default trong `config.json`.
- Không Channel Bible → báo 1 dòng: "Cần Channel Bible để tiếp tục. Gõ @new-channel hoặc cung cấp channel-bible.md."
- Chữ ngoài prompt: tiếng Việt. Prompt asset: tiếng Anh. Lời đọc: ngôn ngữ trong Channel Bible.
- Tự kiểm tra trước khi xuất — sai thì sửa trong cùng lượt.

---

## Pipeline: 5 Giai đoạn

### Phase 1 — Khởi tạo & Lịch trình

**Trigger**: User gõ `@new-channel`, `@new-video`, hoặc bắt đầu chat mới với "bắt đầu video mới".

1. **Đọc trạng thái**: Tìm `channels/<active_channel>/config.json` và `schedule.md`.
   - Chưa có channel → hỏi tên channel, chạy `@new-channel`.
   - Đã có → đọc video kế tiếp trong schedule (dòng ⬜ đầu tiên).
2. **Khởi tạo video mới**: Chạy `@new-video <slug>`, tạo cấu trúc thư mục:
   ```
   channels/<channel>/videos/<slug>/
   ├── script.md
   ├── broll-plan.md
   ├── audio/
   ├── assets/
   └── subtitles/
   ```
3. **Xuất thông tin**: Hiển thị 1 dòng status: `[Channel: <name> | Video: <slug> | Bước: Phase 2 — Kịch bản]`

**Lịch trình (schedule.md) format:**
```
LỊCH TRÌNH — <tên kênh>
CẤU HÌNH: Ngôn ngữ: vi | Độ dài: 8 phút | TTS: vieneu | Voice: Hải Đăng | PACE: 4 từ/giây

| # | Slug | Tiêu đề tạm | Trụ | Phút | Trạng thái |
|---|---|---|---|---|---|
| 1 | ai-thay-doi-giao-duc | AI thay đổi giáo dục | Công nghệ | 8 | ⬜ |
```

- Chưa có lịch trình: khởi tạo 7 video đầu rồi làm luôn video 1. Trụ nội dung, tỉ lệ, công thức tiêu đề, độ dài lấy từ Channel Bible. Hai video liền nhau không cùng trụ, không cùng kiểu hook.
- Đã có: video kế = dòng ⬜ đầu tiên (hoặc số user chỉ định). Tất cả đã ✅ thì thêm 7 video mới (nối số) rồi làm video kế.
- Giao xong cảnh cuối của một video: cập nhật schedule (✅ cho video đó). Chỉ đánh ✅ khi đã giao đủ mọi cảnh.

---

### Phase 2 — Kịch bản (Script)

**Trigger**: `@gen-script "chủ đề"` hoặc sau Phase 1.

**Quy trình:**
1. Đọc Channel Bible (beat structure, % thời lượng, giọng, từ cấm).
2. Ngầm lập **toàn bộ danh sách scene** (beat, loại cảnh, lời đọc ước tính).
3. Tự kiểm tra mỗi scene:
   - Đếm từ ≤ trần của duration dự kiến (4s→12 từ, 6s→18, 8s→24, 10s→29 với tiếng Việt)
   - Không từ cấm, không dính NEGATIVE LIST
4. Xuất `script.md` với format:

```markdown
# Script — <slug>
Ngôn ngữ: vi | Mục tiêu: 8 phút | TTS: vieneu | Voice: Hải Đăng

## Scene 001
- Beat: Hook
- Loại dự kiến: AIV
- Duration ước tính: 6s
- Narration: "Nội dung lời đọc của scene này."

## Scene 002
...
```

5. Hiển thị tóm tắt bảng scenes và hỏi: "Kịch bản ổn không? Sửa thì gõ `@edit-scene N 'nội dung mới'`. Tiếp thì gõ `@gen-audio --all`."

**Lệnh hỗ trợ**: `@show-script`, `@edit-scene N "..."`, `@gen-script "chủ đề" -minutes N`

**Quy tắc hook**: Hook tò mò và hứa cụ thể; lời hứa kiểm chứng được; beat và % thời lượng theo Channel Bible; giọng/xưng hô/từ cấm theo Channel Bible; không dùng lại câu chữ của kênh mẫu.

**Dữ kiện**: Chỉ lấy từ Fact Sheet/notebook đính kèm. Chưa có nguồn thì dùng ví dụ minh họa hoặc nói định tính. Bắt buộc nêu mà chưa có nguồn: thêm đúng một dòng "CẦN NGUỒN: ..." cuối lượt.

---

### Phase 3 — Audio-First (TTS + Timing) ⭐ TRỌNG TÂM

**Trigger**: `@gen-audio --all` hoặc `@gen-audio -scene N`.

#### Bước 3.1 — Tạo Audio

1. Kiểm tra VieNeu-TTS: `@health` (check port 8000).
2. **Nếu online**: Dispatch `scripts/tts-generate.ps1` (Windows) hoặc `scripts/tts-generate.sh` (Linux) cho từng scene, dùng voice từ config.
3. **Nếu offline**: Xuất text TTS đầy đủ (theo profile trong `resources/tts-profiles.md`) và hướng dẫn user đặt file `.wav` vào `audio/S###_narration.wav`.
4. Kết quả: `channels/<channel>/videos/<slug>/audio/S###_narration.wav` cho mỗi scene.

**TTS text rules — theo engine trong CẤU HÌNH:**

**vieneu (VieNeu-TTS) — engine mặc định:**
- API: `localhost:8000` (OpenAI-compatible)
- Default voice: `Hải Đăng`, fallback → `Binh`
- Số, tiền, %, viết tắt → viết ra chữ như đọc (15 triệu → "mười lăm triệu")
- Tags hỗ trợ: `[cười]` `[thở dài]` `[hắng giọng]` — dùng tiết kiệm
- Cảm xúc: dùng câu ngắn, dấu phẩy, `...`, `—` để gợi cảm xúc
- Mỗi câu ≤ 256 ký tự

**gemini-3.8:**
- Không dùng tag ngoặc vuông `[...]`
- Tags góc nhọn cho sự kiện tức thời: `<short pause>` `<long pause>` `<sigh>` `<laugh>` `<breath>` `<gasp>`
- `<short pause>` giữa các câu/ý; `<long pause>` trước số hoặc câu chốt, tối đa 1 lần mỗi 3 cảnh
- Cảm xúc/giọng qua STYLE (tiếng Anh, ≤ 8 từ), đặt trên mỗi khối; gom ít khối nhất có thể

**gemini-3.1:**
- Tags ngoặc vuông, tiếng Anh
- Cảm xúc: `[neutral]` `[calm]` `[curious]` `[serious]` `[tension]` `[hope]` `[frustration]` `[amusement]` `[awe]` `[excited]`
- Nhịp: `[slow]` `[fast]` · Khoảng lặng: `[short pause]` ≈0.25s · `[medium pause]` ≈0.5s · `[long pause]` ≥1s
- Mỗi đoạn mở bằng 1 tag cảm xúc; `[long pause]` tối đa 1 lần mỗi 3 cảnh; không để tag sát tag

#### Bước 3.2 — Phân tích Timing

1. Sau khi có audio, dispatch `scripts/audio-analyze.py` cho từng scene:
   ```
   python audio-analyze.py <audio_file> <output_json> --model base --language vi
   ```
2. Xuất `S###_timing.json`:
   ```json
   {
     "duration_ms": 6320,
     "word_count": 18,
     "words": [
       {"word": "Năm", "start_ms": 120, "end_ms": 390},
       ...
     ]
   }
   ```
3. Cập nhật `script.md`: điền `duration_ms` thực tế vào từng scene.

**Lệnh**: `@analyze --all`, `@timing -scene N`

---

### Phase 4 — B-roll Planning & Review Gate

**Trigger**: `@plan-broll` (sau khi đã có timing JSON cho tất cả scenes).

#### Bước 4.1 — Phân tích Visual Beats

Với mỗi scene, agent **đọc narration text + timing data** và xác định **visual beats** — các điểm chuyển ý cần đổi hình ảnh:

**Logic phân tích:**
- Mỗi câu độc lập hoặc cụm từ mô tả hình ảnh khác nhau = 1 visual beat
- Nhân vật/địa điểm/sự kiện khác nhau = visual beat khác nhau
- Tối thiểu: 1 visual beat / scene
- Tối đa: Phụ thuộc thời lượng narration thực tế

**Chiến lược phân bổ Asset (Cost-Effective Hybrid Pipeline) ⭐:**
Để tối ưu chi phí credit AI (tiết kiệm 70%–85% chi phí):
1. **0s – 30s (Hook Beat & Giữ chân)**: Bắt buộc dùng **AIV (AI Video)** (4s/6s/8s/10s). 30 giây đầu quyết định thuật toán YouTube đề xuất, cần hoạt họa chuyển động mạnh nhất.
2. **Sau 30s (Body & Solution)**:
   - **GFX (Remotion / Hyperframe Motion Graphics — 0 Credit)**: Gán cho cảnh có số liệu, tiền bạc, biểu đồ, so sánh 2 cột, bảng chi phí cơ hội, mũi tên xu hướng. Remotion sẽ tự vẽ animation bằng code (React/SVG/Canvas).
   - **IMG (Ảnh tĩnh AI + Remotion Camera Motion)**: Gán cho cảnh kể chuyện, mô tả bối cảnh, tâm trạng nhân vật. Sinh 1 ảnh tĩnh chất lượng cao (Midjourney/Flux) rồi Remotion áp hiệu ứng camera chuyển động mượt mà (Ken Burns, Slow Zoom In/Out, Pan, Tilt).
   - **AIV (AI Video)**: Chỉ giữ lại ở 1–2 bước ngoặt cảm xúc kịch tính nhất (Climax beat).

**Ví dụ:**
```
Narration scene 5: "Năm 1969, con người đặt chân lên Mặt Trăng.
                    Neil Armstrong bước xuống thang tàu.
                    Hàng triệu người dán mắt vào màn hình TV."

→ 3 visual beats:
  Beat A (0–2.1s):  "Năm 1969... Mặt Trăng" → Tên lửa phóng (AIV 4s snap → thực 2.1s)
  Beat B (2.1–4.8s): "Neil Armstrong..." → Phi hành gia bước xuống (AIV 4s snap → 2.7s)
  Beat C (4.8–6.3s): "Hàng triệu người..." → Đám đông xem TV (AIV 4s snap → 1.5s)
```

**Snap duration về hằng số AIV**: Dùng timing thực từ Whisper để xác định beat boundaries, sau đó:
- Tổng duration của scene = `duration_ms` thực tế
- Phân chia thời gian cho từng B-roll:
  - Cảnh **AIV**: Ưu tiên snap vào hằng số {4, 6, 8, 10}s
  - Cảnh **IMG / GFX**: Linh hoạt theo nhịp câu (2s – 12s), không ép buộc vào hằng số AIV
- Nếu beat quá ngắn (< 3s) → gộp với beat liền kề hoặc dùng hiệu ứng Text Pop-up trong Remotion

#### Bước 4.2 — Xuất B-roll Plan

Ghi `broll-plan.md` và `broll-plan.json` (kèm định dạng Remotion renderer props nếu có GFX/IMG):

```markdown
# B-roll Plan — <slug>
Status: DRAFT (chờ @approve-broll) | Chiến lược: Hybrid Cost-Saver

## Scene 001 | Beat: Hook (0s-6s) | Duration: 6.3s | Narration words: 18

| B-roll | Type | Duration | Description | Camera / Renderer |
|---|---|---|---|---|
| S001-A | AIV | 6s | Hook opening shot | CU, push-in, Storyboard 3 panels |

## Scene 004 | Beat: Số liệu (45s-53s) | Duration: 8s

| B-roll | Type | Duration | Description | Camera / Renderer |
|---|---|---|---|---|
| S004-A | GFX | 4s | Biểu đồ nợ thẻ tăng vọt | Remotion: ChartMotion |
| S004-B | IMG | 4s | Bàn tay cắt đôi thẻ tín dụng | Remotion: Ken Burns Zoom-in |
```

#### Bước 4.3 — Review Gate ⛔

**DỪNG LẠI** và hiển thị:
```
📋 B-roll Plan đã sẵn sàng. Hãy review:

[Hiển thị bảng tóm tắt]

Lệnh:
  @show-broll           — xem chi tiết đầy đủ
  @edit-broll S003 ...  — chỉnh sửa
  @approve-broll        — duyệt và chuyển sang Phase 5
```

**Chỉ sau `@approve-broll` mới tiếp tục sang Phase 5.**

---

### Phase 5 — Asset Prompts & Subtitle

**Trigger**: `@gen-prompts --all` (sau `@approve-broll`).

#### Bước 5.1 — Tạo Asset Prompts

Dòng nhắc cố định ngay trên bảng prompt: "📌 Flow: tạo xong asset nào thì ĐỔI TÊN ngay đúng cột Tên file (thứ tự cảnh tăng dần), rồi mới tải về."

Với mỗi B-roll trong plan đã duyệt, tạo bảng: `| Tên file | Prompt | Storyboard |`

**Cảnh AIV** — 2 dòng liền nhau (storyboard _sb.png trước, clip .mp4 sau):

```
Tên file: S001-A_4s_AIV_sb.png
Prompt: [Mô tả storyboard từng khung theo thứ tự thời gian.
         Panel 1 (0-2s): ... Panel 2 (2-4s): ...]
        <STYLE LOCK nguyên văn từ Channel Bible>
        Avoid: <NEGATIVE LIST ≤25 từ>

Tên file: S001-A_4s_AIV.mp4
Prompt: Use the attached storyboard image as the shot plan: animate panel 1 through panel N
        in order, with the timings below, as ONE continuous full-frame N-second shot.
        Do not show panel borders, a grid or multiple panels.
        [Mô tả chuyển động từng khung; không thêm chủ thể hay bối cảnh ngoài storyboard]
        Audio: only natural ambient sound and scene sound effects; no music, no speech,
        no dialogue, no singing, no narration; characters never speak and keep their mouths closed.
        <STYLE LOCK nguyên văn>
        Avoid: <NEGATIVE LIST>
```

**Cảnh IMG** — 1 dòng .png, không storyboard:
```
Tên file: S002_IMG.png
Prompt: [Mô tả ảnh tĩnh. Cỡ cảnh, góc máy, chủ thể, bối cảnh]
        <STYLE LOCK nguyên văn>
        Avoid: <NEGATIVE LIST>
```

**Cảnh GFX** — 1 dòng .png (đồ họa chuyển động áp bằng phần mềm):
```
Tên file: S005_GFX.png
Prompt: [Mô tả đồ họa/infographic tĩnh. Chuyển động sẽ thêm trong phần mềm dựng.]
        <STYLE LOCK nguyên văn>
        Avoid: <NEGATIVE LIST>
```

**Naming convention (quan trọng):**
- `S{NNN}-{beat}_{dur}s_{type}[_sb].{ext}` — ví dụ: `S001-A_4s_AIV_sb.png`, `S001-A_4s_AIV.mp4`, `S003_IMG.png`
- Không có prefix video (vì đã nằm trong folder video riêng)
- KHÔNG nhét tên file vào nội dung prompt (model sẽ vẽ chữ lên hình)

**Storyboard (số khung theo duration):**
- 4s → 2 khung · 6s → 3 khung · 8s → 4 khung · 10s → 4 khung (lưới 2×2)
- Một ảnh ngang 16:9, viền khung mảnh, KHÔNG chữ/số/mũi tên trong ảnh
- Các khung cùng bối cảnh, nhân vật, ánh sáng; chỉ khác phần thay đổi theo thời gian
- Cỡ cảnh/góc máy/chuyển động theo `references/camera-vocabulary.md`
- Cột Storyboard (chỉ điền ở dòng _sb): ghi tiếng Việt từng khung — `K1 · hành động · cỡ cảnh · góc/máy · 0–2s`; tổng giây các khung = dur

**Quy tắc prompt:**
- Không mô tả nhân vật nói, hát, hô hay mở miệng như đang nói
- Nhân vật hoặc biểu tượng lặp lại: dùng đúng một mô tả cố định mỗi lần
- Không chữ trên hình trừ khi Channel Bible cho phép
- Prompt clip ghi rõ "N-second clip" và chuyển động diễn ra đủ N giây
- Tách ý dài thành nhiều cảnh: đổi ít nhất 2 trong 3 yếu tố (cỡ cảnh, góc máy, chuyển động)
- Hơn 3 cảnh liền cùng thời lượng → đổi bớt khi lời đọc cho phép

#### Bước 5.2 — Sinh Subtitle Karaoke

Dispatch `scripts/subtitle-gen.py`:
```
python subtitle-gen.py <audio_dir> <subtitles/karaoke.srt> --format srt --group-size 4
```

Xuất `channels/<channel>/videos/<slug>/subtitles/karaoke.srt`

Hỗ trợ: `@gen-subs --format ass` (với word-highlight màu), `@preview-subs -scene N`

#### Bước 5.3 — Shot List cuối

Xuất bảng shot list đầy đủ hiển thị trong chat:

```
📌 Shot List — <slug>
Ngôn ngữ: <...> | Mục tiêu: <...> phút | Tổng thời lượng AI video: <...>s | Số cảnh: <...>

[Bảng: Scene | File | Duration | Type | Beat | Prompt (tóm tắt 1 dòng) | Storyboard]
```

Format khối cảnh đầy đủ (theo `references/shot-list.template.md`):
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

#### Bước 5.4 — Xuất Remotion Composition (@gen-remotion)

Nếu B-roll plan có cảnh `IMG` hoặc `GFX`, Agent có thể xuất cấu trúc Remotion composition:
```
channels/<channel>/videos/<slug>/assets/remotion-composition.json
```
Chứa toàn bộ danh sách sequences, components (`ChartMotion`, `CounterNumber`, `KenBurnsImage`), timing frame (30fps), và props để Remotion render trực tiếp thành video hoàn chỉnh hoặc graphic overlays.

---

## Tự kiểm tra (checklist ngầm trước mỗi lượt xuất)

- [ ] Mỗi cảnh AIV duration ∈ {4, 6, 8, 10}s
- [ ] Số từ narration ≤ trần: 4s→12, 6s→18, 8s→24, 10s→29 (tiếng Việt); 4s→9, 6s→14, 8s→19, 10s→24 (tiếng Anh)
- [ ] Cuối video: tổng thời lượng = tổng các cảnh và trong ±5% mục tiêu
- [ ] Mọi prompt có STYLE LOCK nguyên văn
- [ ] Mọi prompt clip có câu Audio (không âm nhạc, không nhân vật nói)
- [ ] Tên file liên tục, không trùng, không hụt; mọi cảnh AIV có ảnh _sb ngay trước clip; số khung đúng quy tắc; tổng giây các khung = dur
- [ ] Số đoạn TTS = số cảnh; tag đúng profile engine đang dùng
- [ ] Không từ cấm, không dính NEGATIVE LIST
- [ ] Cắt cảnh đúng cuối câu, không cắt giữa mệnh đề
- [ ] Không lặp clip, không kéo giãn clip

---

## Lệnh điều khiển nhanh

| User gõ | Agent làm |
|---|---|
| `tiếp` hoặc `@next` | Bước tiếp theo trong pipeline |
| `@undo` | Quay lại bước trước |
| `sửa cảnh N: ...` hoặc `@edit-scene N "..."` | Sửa narration scene N |
| `sửa style: ...` hoặc `@set-style ...` | Cập nhật STYLE LOCK |
| `@pipeline --from audio` | Chạy lại từ bước audio |
| `@pipeline --from broll` | Chạy lại từ bước B-roll |
| `@pipeline --from prompts` | Chạy lại từ bước sinh prompt |
| `seo` | Xuất tiêu đề SEO, mô tả, tags |
| `thumbnail` | Xuất prompt thumbnail |
| `checklist` | Xuất assembly checklist |
| `@cheatsheet` | Xem toàn bộ cheatcodes |
| `@health` | Kiểm tra services |
| `@status` | Trạng thái channel + video hiện tại |
| `@config` | Xem toàn bộ config hiện tại |
| `@schedule show` | Xem lịch trình |
| `@shot-list` | Xuất shot list đầy đủ |

---

## Ràng buộc thời lượng (TUYỆT ĐỐI, ưu tiên cao nhất)

> Absolute AI video constants: **4s / 6s / 8s / 10s** — never arbitrary seconds, never loop video.
> Narration word count (tiếng Việt, mỗi tiếng = 1 từ): 4s ≤ 12, 6s ≤ 18, 8s ≤ 24, 10s ≤ 29.
> Tiếng Anh: 4s ≤ 9, 6s ≤ 14, 8s ≤ 19, 10s ≤ 24.
> Ảnh tĩnh (IMG) và đồ họa (GFX): linh hoạt thời lượng — tối đa 12s (số từ ≤ 12 × PACE); dài hơn thì tách cảnh.
> Nếu CẤU HÌNH ghi "Ảnh tĩnh miễn: không" thì áp dụng hằng số AIV cho mọi cảnh.
> Không lặp clip, không kéo giãn clip để lấp thời lượng. Lời dài hơn clip thì rút lời, không kéo clip.

---

## Tham chiếu

- **Camera Vocabulary**: `references/camera-vocabulary.md`
- **Channel Bible Template**: `references/channel-bible.template.md`
- **Shot List Template**: `references/shot-list.template.md`
- **Assembly Checklist**: `references/assembly-checklist.md`
- **TTS Profiles**: `resources/tts-profiles.md`
- **Cheatcode Registry**: `resources/cheatcodes.json`
