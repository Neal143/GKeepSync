# Phase 04: Chức năng Khởi động cùng Windows (Run on Startup)
Status: ✅ Complete
Dependencies: Phase 03

## Objective
Tích hợp tính năng cho phép ứng dụng GKeepSync tự khởi động mỗi khi người dùng đăng nhập vào Windows. Cần có tùy chọn (checkbox) trong giao diện để bật/tắt tính năng này tùy ý. Kèm theo đó, ứng dụng khi khởi động theo cách này sẽ bật lên màn hình to ngay lập tức theo yêu cầu của User.

## Requirements
### Functional
- [ ] Thêm một Checkbox "Tự khởi động cùng Windows" vào `main_frame.py` (Khu vực Cấu Hình là hợp lý nhất).
- [ ] Trạng thái của Checkbox được lưu vào `config.json`.
- [ ] Xử lý logic tạo/xóa Registry Key (hoặc file `.lnk` trong thư mục Startup) ở hệ điều hành Windows khi người dùng tick/bỏ tick Checkbox.

### Non-Functional
- [ ] App mở lên mặc định là màn hình chính Tkinter (không thu nhỏ ban đầu) khi start up cùng máy tính, đúng như Brief.
- [ ] Không yêu cầu quyền Administrator nếu dùng Registry `HKEY_CURRENT_USER` hay thư mục Startup `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup`.

## Implementation Steps
1. [x] Viết helper function trong `utils/os_utils.py` (nếu có, hoặc tạo mới) để:
   - `enable_startup()`
   - `disable_startup()`
   - `check_startup_status()`
2. [x] Gắn UI Checkbox vào giao diện, def callback khi check/uncheck.
3. [x] Test độc lập tính năng thêm/xóa khỏi Registry/Thư mục Startup.

## Files to Create/Modify
- `ui/frames/main_frame.py` (UI Checkbox).
- `utils/os_utils.py` (chức năng Registry/Startup link).

## Test Criteria
- [ ] Tick chọn -> Kiểm tra xem registry key/lnk có được tạo thành công không với đường dẫn đúng đến file `.exe` (hoặc `.py` đang chạy dev).
- [ ] Khởi động lại máy -> App tự chạy và hiện cửa sổ to.
- [ ] Bỏ tick -> System xóa key/lnk thành công.
- [ ] Khởi động lại máy lần 2 -> App không tự chạy.

## Notes
Vì đang test dưới dạng source code python (.py), đường dẫn trong registry sẽ trỏ về `python.exe d:/.../app.py`. Khi build sang exe sẽ trỏ về `app.exe`. Cần viết hàm `sys.argv[0]` kết hợp hàm build nhận diện (`getattr(sys, 'frozen', False)`) linh hoạt cho cả 2 môi trường.

---
Next Phase: Phase 05
