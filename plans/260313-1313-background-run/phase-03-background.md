# Phase 03: Chức năng Chạy Ngầm (Background / System Tray)
Status: ✅ Complete
Dependencies: Phase 02

## Objective
Cho phép cửa sổ chính (Tkinter) thu nhỏ thay vì thoát hoàn toàn, duy trì một Icon chạy ngầm dưới System Tray (Taskbar) để người dùng điều khiển được ứng dụng.

## Requirements
### Functional
- [ ] Chặn hành vi bấm phím close/chéo (`[X]`) mặc định của cửa sổ chính Tkinter.
- [ ] Thu nhỏ hoặc ẩn (`withdraw()`) cửa sổ chính.
- [ ] Khởi tạo 1 System Tray Icon bằng `pystray`.
- [ ] System Tray Icon này cần có context menu 3 nút: **Mở App** (hiện lại cửa sổ `deiconify()`), **Đồng bộ ngay** (gọi hàm start_sync), **Thoát hẳn app** (Hủy system tray và destroy Tkinter window an toàn).

### Non-Functional
- [ ] Đảm bảo luồng Syncing đang chạy không bị ngắt quãng vô lý khi Hide/Show form.
- [ ] Hiển thị nhắc nhở nhỏ (Notification) khi lần đầu ẩn app (Tùy chọn phụ trợ nhưng không bắt buộc, vì User chọn "không hỏi han lằng nhằng". Cân nhắc nếu thấy phù hợp UX).

## Implementation Steps
1. [x] Sửa đổi handler `protocol("WM_DELETE_WINDOW")` trong `app.py`.
2. [x] Viết hàm `hide_window()`: 
   - Ẩn cửa sổ (`self.withdraw()`).
   - Khởi tạo thread hoặc setup pystray Icon.
3. [x] Viết hàm `show_window(icon, item)`:
   - Dừng icon (`icon.stop()`).
   - Hiện cửa sổ (`self.deiconify()`).
   - Focus lại các cửa sổ chính.
4. [x] Khớp action "Đồng bộ ngay" vào system tray menu.

## Files to Create/Modify
- `app.py` -> Nắm chính logic pystray và window hiding.
- icon file (VD: `assets/icon.ico` hoặc `assets/icon.png` cho `pystray`).

## Test Criteria
- [ ] Bật app -> bấm X -> cửa sổ biến mất, dưới góc phải hiện icon của app.
- [ ] Bấm đúp hoặc chuột phải chọn "Mở App" -> cửa sổ hiện lên ở vị trí cũ, icon góc phải biến mất.
- [ ] Chuột phải chọn "Thoát hẳn App" -> Chương trình terminate sạch sẽ trong Task Manager.

## Notes
Tkinter và pystray đôi chút khó chịu nếu loop trên cùng main thread. Cần thiết kế: `pystray` run() có thể block main thread, nên có thể chạy Tkinter trong another queue/thread, hoặc `pystray` chạy detached thread tùy API.

---
Next Phase: Phase 04
