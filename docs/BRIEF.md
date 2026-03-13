# 💡 BRIEF: GKeepSync

**Ngày tạo:** 2026-03-06
**Cập nhật lần cuối:** 2026-03-14
**Loại sản phẩm:** Desktop App (Windows .exe)

---

## 1. VẤN ĐỀ CẦN GIẢI QUYẾT
Google Keep không hỗ trợ export/backup ghi chú ra file dễ dàng. Người dùng muốn:
- Backup ghi chú về máy tính phòng mất dữ liệu
- Tìm kiếm và lọc ghi chú offline theo tag, thời gian
- Có bản sao local dạng Markdown để dùng với các tool khác

## 2. GIẢI PHÁP ĐỀ XUẤT
App Windows với giao diện đồ họa (CustomTkinter), sử dụng `gkeepapi` để kết nối Google Keep qua Master Token, sync ghi chú về thư mục local dưới dạng file `.md`.

## 3. ĐỐI TƯỢNG SỬ DỤNG
- **Primary:** Người dùng Google Keep muốn backup/quản lý ghi chú offline
- **Secondary:** Người dùng muốn chuyển ghi chú sang hệ thống Markdown-based (Obsidian, Notion...)

## 4. CÔNG NGHỆ
| Thành phần | Công nghệ |
|---|---|
| Ngôn ngữ | Python 3.x |
| GUI | CustomTkinter |
| Google Keep API | gkeepapi |
| Auth | Master Token (qua gpsoauth) |
| Build .exe | PyInstaller |

## 5. TÍNH NĂNG

### 🚀 MVP (Bắt buộc có):
- [x] Đăng nhập bằng Master Token
- [x] Sync ghi chú Keep → thư mục local (file `.md`)
- [x] Lọc ghi chú theo **tag/label**
- [x] Lọc theo **khoảng thời gian** (từ ngày → đến ngày)
- [x] **Auto Sync** theo thời gian cài đặt (15 phút / 1 giờ / 6 giờ / tùy chỉnh)
- [x] **Manual Sync** bấm nút sync bất cứ lúc nào
- [x] Xem danh sách ghi chú đã sync trong app
- [x] Chọn thư mục lưu ghi chú
- [x] Thông báo khi sync xong / gặp lỗi

### ⭐ Tính năng nâng cao (Đã hoàn thành):
- [x] **Đăng nhập qua Chrome Extension (OAuth):** Nhận token từ Extension qua Local HTTP Server.
- [x] **Tích hợp NotebookLM:** Tự động đẩy ghi chú đã sync lên Notebook chỉ định.
- [x] **System Tray:** App thu nhỏ về góc màn hình thay vì đóng hẳn khi nhấn [X]. Menu chuột phải: Mở App / Sync Ngay / Thoát.
- [x] **Windows Startup:** ứng dụng tự khởi động cùng Windows qua Startup Folder, chạy ngầm không hiện cửa sổ.

## 6. ƯỚC TÍNH SƠ BỘ
- **Độ phức tạp:** Trung bình
- **Rủi ro:**
  - `gkeepapi` là thư viện không chính thức, Google có thể chặn bất cứ lúc nào
  - Master Token cần lấy thủ công, hơi phức tạp cho người mới
  - Google thay đổi API → app có thể ngừng hoạt động

## 7. BƯỚC TIẾP THEO
→ Duyệt Brief → Chạy `/plan` để thiết kế chi tiết → `/code` để implement
