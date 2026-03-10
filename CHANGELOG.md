# Changelog

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
