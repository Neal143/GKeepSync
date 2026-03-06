# Phase 02: Core Engine (Keep Client + Sync)
Status: ⬜ Pending
Dependencies: Phase 01

## Objective
Xây dựng logic core: kết nối Google Keep, lấy notes, convert sang Markdown, sync về thư mục local.

## Implementation Steps
1. [ ] `keep_client.py` — Wrapper cho gkeepapi:
   - Login bằng email + Master Token
   - Lấy tất cả notes (hoặc lọc theo label/thời gian)
   - Trả về danh sách note objects
2. [ ] `utils/markdown_converter.py` — Convert note → file .md:
   - Title → filename (sanitize ký tự đặc biệt)
   - Content → markdown body
   - Labels → YAML frontmatter tags
   - Timestamps → frontmatter metadata
   - Checklist items → markdown checkboxes
3. [ ] `sync_engine.py` — Logic đồng bộ:
   - So sánh notes từ Keep với files local (by note ID)
   - Tạo file mới / cập nhật file đã thay đổi
   - Tracking sync state (lưu last sync time, note ID mapping)
   - Auto sync scheduler (dùng threading.Timer)
   - Callback cho UI (progress, status, errors)

## Files to Create
- `keep_client.py`
- `sync_engine.py`
- `utils/markdown_converter.py`

## Test Criteria
- [ ] Login với Master Token thành công
- [ ] Lấy được danh sách notes
- [ ] Convert note → file .md đúng format
- [ ] Sync tạo đúng files trong thư mục target
- [ ] Auto sync chạy đúng interval
