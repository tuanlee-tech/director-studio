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

> [!NOTE]
> Skill đang trong quá trình triển khai. Phần nội dung chi tiết sẽ được hoàn thiện ở Phase 4.

## Triết lý Audio-First

Giọng đọc (narration) là trục chính. Tạo audio trước → đo timing chính xác → từ đó
quyết định subtitle karaoke và số lượng/thời lượng B-roll phù hợp.

## Cheatcode API

Gõ `@cheatsheet` để xem danh sách đầy đủ các lệnh ngắn có thể dùng.

## TODO (Phase 4)
- [ ] OS Detection & Script Dispatch logic
- [ ] Phase 1-5 full workflow
- [ ] Audio-First pipeline chi tiết
- [ ] Visual beats analysis
- [ ] B-roll planning & Review Gate
- [ ] Asset prompt generation
