# Phase 02: Login Flow (App + Ext)
Status: ⬜ Pending | 🟡 In Progress | ✅ Complete
Dependencies: Phase 01

## Objective
Triển khai giao diện Màn Hình Đăng Nhập (LoginFrame) gờm 2 tab và xây dựng toàn bộ luồng kết nối nhận Master Token từ Chrome Extension thông qua Localhost Server.

## Requirements
### Functional
- [x] Xây dựng `LoginFrame` với 2 Tab (UI Browser vs UI Thủ công).
- [x] Tích hợp Token Server (Flask/FastAPI micro server) chạy ngầm để lắng nghe cổng `12345` chờ Token.
- [x] Xây dựng Extension Popup UI dựa trên chuẩn Material 3 (Nhỏ gọn, Status Label).
- [x] Xây dựng luồng Logic `exchange_oauth_for_master` để đổi thẻ.
- [x] Cơ chế Tự Động Lưu Phiên: Lưu Token và Email vào config.

### Non-Functional
- [x] Hiện Loading State, khóa nút khi Click "Kết nối", tránh bắn HTTP Request liên tục.
- [x] Error Handling: Xử lý mượt mà khi lỗi auth -> Trả Toast đỏ cảnh báo.

## Implementation Steps
1. [x] Viết `LoginFrame` bọc trong Card góc bo tròn trên màn hình nền xám.
2. [x] Cấu hình Token Server trong `core/token_server.py`.
3. [x] Cập nhật Chrome Extension HTML/JS hiển thị UI mới.
4. [x] Viết chức năng Auto-Login (Bypass Login Frame nếu có lưu config cũ).

## Files to Create/Modify
- `ui/login_frame.py` - Màn hình đăng nhập đa luồng.
- `core/token_server.py` - REST Endpoint nhận token Extension.
- `extension_v2/popup.html` & `popup.js` - Chrome Extension.

---
Next Phase: phase-03-keep-local.md
