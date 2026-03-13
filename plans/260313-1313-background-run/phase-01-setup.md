# Phase 01: Setup & Phân tích cấu trúc file
Status: ✅ Complete
Dependencies: None

## Objective
Kiểm tra cấu trúc file hiện tại, đảm bảo đã cài đặt đủ thư viện cần thiết (`pystray`, `Pillow` cho icon...) và phân tách phần GUI Tkinter ra khỏi logic xử lý ngầm (nếu cần).

## Requirements
### Functional
- [ ] Phân tích file `app.py` và `main_frame.py` để tìm điểm chèn logic startup và close app.
- [ ] Đảm bảo `config.json` hoặc cơ chế tương tự đã tồn tại và sẵn sàng cho việc mở rộng (thêm key cho thư mục và notebook).
- [ ] Cài đặt thư viện `pystray` (nếu chưa có).

### Non-Functional
- [ ] Không làm gãy flow hiển thị UI ban đầu.

## Implementation Steps
1. [x] Đọc cấu trúc `app.py` (điểm entry).
2. [x] Đọc hàm xử lý lúc đóng cửa sổ (ví dụ: `protocol("WM_DELETE_WINDOW")` của Tkinter).
3. [x] Cập nhật `requirements.txt` bằng thư viện mới.

## Files to Create/Modify
- `requirements.txt` - Thêm `pystray`, `Pillow`.
- Tập lệnh liên quan UI chính.

## Notes
Phase này tập trung vào khảo sát và chuẩn bị móng. Sẽ thực hiện sau khi user gọi `/design` hoặc `/code phase-01`.

---
Next Phase: Phase 02
