# 💡 BRIEF: Tính năng Khởi động cùng Windows & Chạy ngầm & Lưu Cấu hình

**Ngày tạo:** 13/03/2026
**Tính năng:** Background Sync & State Persistence
**Nhánh (Branch):** `feat/background-run`

---

## 1. VẤN ĐỀ CẦN GIẢI QUYẾT
- Hiện tại, mỗi lần mở app lên người dùng phải chọn lại đúng thiết lập Đồng bộ (từ thư mục Local nào lên Google Keep Notebook nào). Việc này mất thời gian và dễ làm sai.
- Người dùng muốn app có thể tự động chạy ngầm để giữ kết nối đồng bộ liên tục mà không bắt buộc phải luôn mở cửa sổ to chình ình trên màn hình. App có thể mở cùng với lúc bật máy tính.

## 2. GIẢI PHÁP ĐỀ XUẤT
Thêm 2 cụm tính năng chính:
1. **Lưu cấu hình (State Persistence):** Tự động lưu lại thiết lập gần nhất (Local Folder <-> Notebook) trước khi tắt app. Khi mở lại app, sẽ tự động load lại đúng thiết lập đó.
2. **Chạy ngầm & Khởi động cùng hệ thống:**
   - App thu nhỏ xuống System Tray (góc phải màn hình dưới) thay vì thoát hẳn khi bấm [X].
   - Có tùy chọn cho phép App tự khởi động khi mở máy tính Windows.

## 3. CHI TIẾT TÍNH NĂNG MỚI

### 🚀 Những phần bắt buộc:
- [ ] **Lưu cấu hình:** Tự động nhớ Notebook và Local Folder đã chọn ở phiên làm việc trước đó.
- [ ] **Khôi phục cấu hình:** Tự động điền lại các thiết lập này ngay khi app vừa khởi động.
- [ ] **Khởi động cùng Windows:** Tự động mở cửa sổ app to lên màn hình chính khi vừa bật máy tính.
- [ ] **Chạy ngầm (Background):**
  - Khi bấm dấu [X] màu đỏ ở góc trên cùng của Titlebar, cửa sổ chính của App tự động thu nhỏ xuống icon dưới góc phải (System Tray), app không hiện cửa sổ nhưng vẫn tiếp tục chạy ngầm.
  - Chuột phải vào icon ở System Tray sẽ hiện menu Context gồm 3 nút tùy chọn duy nhất: Mở App, Đồng bộ ngay, Thoát hẳn App.

## 4. ƯỚC TÍNH SƠ BỘ
- **Độ phức tạp:** Trung bình - Cần can thiệp vào cách khởi tạo của `customtkinter` và sửa logic lưu file `config.json`.
- **Rủi ro:** 
  - Đóng app đột ngột có thể lỗi file config.
  - Xử lý System Tray trên Windows đôi khi bị sót icon (phantom icon) khi thoát app không sạch.
  - Xung đột giữa luồng Sync bất đồng bộ và việc ẩn/hiện cửa sổ Tkinter.

## 5. BƯỚC TIẾP THEO
→ Chạy `/plan` để lên thiết kế chi tiết luồng hoạt động (Sequence Flow) của tính năng.
