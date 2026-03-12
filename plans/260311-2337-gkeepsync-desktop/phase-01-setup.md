# Phase 01: Setup & Base Layout
Status: ⬜ Pending | 🟡 In Progress | ✅ Complete
Dependencies: None

## Objective
Thiết lập bộ khung dự án (Boilerplate) bằng CustomTkinter và xây dựng layout 2 cột (Sidebar & Content Area). Khởi tạo hệ thống Theme và File cấu hình (config.json).

## Requirements
### Functional
- [x] Khởi tạo ứng dụng `app.py` với cấu trúc Class cơ bản.
- [x] Xây dựng Sidebar cố định bên trái chứa 4 nút Menu điều hướng.
- [x] Xây dựng vùng Content bên phải theo cơ chế thay đổi View (Chưa cần chức năng từng View).
- [x] Tạo file `config_manager.py` đọc/ghi `config.json` để lưu trữ cài đặt.

### Non-Functional
- [x] Tuân thủ thiết kế Material 3: Màu nền `#F5F5F7`, Sidebar nền `#FFFFFF` có đổ bóng ảo (border viền xám mờ).
- [x] Định nghĩa sẵn các hằng số màu sắc (Color Tokens) cho toàn bộ App.

## Implementation Steps
1. [x] Trích xuất các biến màu từ `UI_UX.md` vào file `ui/themes/colors.py`.
2. [x] Viết lớp `MainFrame` chứa `Sidebar` (Tĩnh) bên trái và vùng Frame đa dụng bên phải.
3. [x] Khởi tạo 4 dummy views: `HomeView`, `KeepView`, `NLMView`, `SyncView` để gắn vào khung chính.

## Files to Create/Modify
- `ui/themes/colors.py` - Chứa mã màu hex.
- `ui/main_frame.py` - Frame chứa Sidebar và cơ chế switch Tab.
- `core/config_manager.py` - Đọc ghi trạng thái JSON.

---
Next Phase: phase-02-login.md
