# Phase 02: Chức năng Lưu và Khôi phục Cấu hình
Status: ✅ Complete
Dependencies: Phase 01

## Objective
Tích hợp khả năng ghi nhớ các thiết lập đồng bộ gần nhất của người dùng (Local Folder path và Google Keep Notebook mặc định) vào file cấu hình cục bộ và tự động điền lại khi mở app.

## Requirements
### Functional
- [ ] Ghi nhận sự thay đổi cấu hình đồng bộ (khi người dùng đổi Local Folder hoặc chọn lại Notebook).
- [ ] Lưu các thay đổi này xuống file `config.json` hoặc sử dụng một file riêng (VD: `session_state.json`) nếu cần.
- [ ] Khi App mở lên, đọc thiết lập và áp dụng thẳng vào giao diện `main_frame` (pre-fill dữ liệu).

### Non-Functional
- [ ] Xử lý an toàn khi file `config.json` bị mất hoặc hỏng (fallback về trạng thái mặc định không lỗi).

## Implementation Steps
1. [x] Cập nhật module quản lý config (`core/auth/` hoặc `utils/` tùy cấu trúc).
2. [x] Thêm logic `save_state()` khi user nhấn nút Sync hoặc khi user thoát ứng dụng.
3. [x] Thêm logic `load_state()` được gọi ngay sau khi `main_frame` init xong.
4. [x] Cập nhật các UI element: text box hoặc label thư mục local, OptionMenu notebook.

## Files to Create/Modify
- `ui/frames/main_frame.py` (chèn pre-fill).
- Một file phụ trách config logic (ví dụ `app.py` hoặc class `ConfigManager` nếu có).

## Test Criteria
- [ ] Mở app lần 1 -> Cấu hình một cái -> Tắt app.
- [ ] Mở app lần 2 -> Cấu hình hiện đúng trạng thái trước đó.

## Notes
Logic này nên thực hiện nhẹ nhàng trước khi gắn System Tray vào để tránh đụng độ luồng tắt.

---
Next Phase: Phase 03
