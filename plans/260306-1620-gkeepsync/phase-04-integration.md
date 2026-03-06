# Phase 04: Integration & Polish
Status: ⬜ Pending
Dependencies: Phase 02, Phase 03

## Objective
Kết nối Core Engine với GUI, xử lý threading, error handling, logging.

## Implementation Steps
1. [ ] Kết nối Login frame → `keep_client.login()`
2. [ ] Kết nối Sync Now → `sync_engine.sync()`
3. [ ] Threading: Sync chạy background, không block UI
4. [ ] Auto sync scheduler integration
5. [ ] Progress callback → cập nhật status bar
6. [ ] Error handling toàn diện:
   - Token hết hạn → hiện thông báo
   - Mất mạng → retry logic
   - File permission errors
7. [ ] `utils/logger.py` — Logging to file
8. [ ] Lưu config (token, settings) vào JSON file
9. [ ] Remember login (auto-login khi mở app lại)
10. [ ] Polish UI: animations, loading states

## Files to Modify
- `app.py` — Wire up UI + Engine
- `config.py` — Persist settings

## Files to Create
- `utils/logger.py`

## Test Criteria
- [ ] Login → Sync → Thấy files trong thư mục
- [ ] Auto sync chạy đúng interval
- [ ] UI không bị đơ khi đang sync
- [ ] Đóng app → mở lại → auto login
- [ ] Error cases hiển thị thông báo đúng
