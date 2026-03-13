# Changelog

## [2026-03-14]
### Added
- **Background Run & System Tray**: Hoàn thiện cơ chế chạy ngầm khi nhấn nút [X]. Tích hợp `TrayManager` quản lý icon và menu ở Taskbar.
- **Windows Startup**: Tự động tạo Shortcut trong thư mục Startup của Windows. Hỗ trợ flag `--start-hidden` để khởi động không hiện cửa sổ.
- **Ghost Window Prevention**: Kỹ thuật `alpha=0.0` giúp triệt tiêu hiện tượng nháy màn hình trắng khi app khởi động ngầm.

### Changed
- **Major Refactor (SRP - Giai đoạn 1)**: Tách toàn bộ logic System Tray (`pystray`, `PIL`) ra khỏi `app.py` vào `ui/tray_manager.py`. `GKeepSyncApp` giờ chỉ đóng vai trò điều phối tinh gọn.
- **Major Refactor (SRP - Giai đoạn 2)**: Giải phóng ~200 dòng code render giao diện khỏi `ui/main_frame.py`. Trách nhiệm vẽ ghi chú, danh sách Notebooks và Log được đẩy về các View chuyên biệt (`KeepView`, `NLMView`, `SyncView`).
- **Tài liệu dự án**: Đồng bộ hóa toàn bộ `PRD.md`, `DESIGN.md`, `UI_UX.md`, `UI_MAPPING.md` với kiến trúc module mới.

### Fixed
- Lỗi Tkinter bị treo/crash khi khởi động ngầm cùng Windows nhờ xử lý luồng `mainloop` và `alpha` chuẩn xác.

## [2026-03-09]

### Added
- Workflow hỗ trợ "1-Click Login" từ Chrome Extension: Tự động trích xuất thông tin đăng nhập Google (`oauth_token`) từ trình duyệt Chrome và nhận lại `master_token` vĩnh viễn. Thiết lập thông qua `token_server.py`.
- Tự động bỏ dấu và loại bỏ ký tự đặc biệt cho Tiếng Việt trong tên File Markdown và tên Tag (`utils.markdown_converter.py`).
- Tính năng đồng bộ tự động lên cấu trúc NotebookLM thông qua `nlm` CLI với Unicode fixes (`utils.nlm_worker.py`).

### Changed
- Refactored KeepClient Authentication logic: Tự động nhận diện cấu trúc Token (App Password vs OAuth Token vs Master Token) để bypass lỗi "Plaintext is too long" và "BadAuthentication" do mã hóa nhầm qua RSA.
- Tối ưu hóa UI Code: Phân rã Class `MainFrame` (`ui/main_frame.py`) thành các hàm build nhỏ (Filters, Header, Notes List).
- Sửa lỗi Pylint `subprocess.run` thiếu tham số `check` và tên biến `logger` trùng lặp trong thư viện cảnh báo.

### Fixed
- Lỗi Google từ chối cookie đăng nhập (BadAuthentication) bằng cách gọi thẳng API `gpsoauth.exchange_token`.
- Lỗi Crash Console do in ký tự có dấu khi gọi ngầm `nlm.exe` trên Windows.
