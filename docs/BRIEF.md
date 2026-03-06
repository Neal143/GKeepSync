# 💡 BRIEF: GKeepSync

**Ngày tạo:** 2026-03-06
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
- [ ] Đăng nhập bằng Master Token
- [ ] Sync ghi chú Keep → thư mục local (file `.md`)
- [ ] Lọc ghi chú theo **tag/label**
- [ ] Lọc theo **khoảng thời gian** (từ ngày → đến ngày)
- [ ] **Auto Sync** theo thời gian cài đặt (15 phút / 1 giờ / 6 giờ / tùy chỉnh)
- [ ] **Manual Sync** bấm nút sync bất cứ lúc nào
- [ ] Xem danh sách ghi chú đã sync trong app
- [ ] Chọn thư mục lưu ghi chú
- [ ] Thông báo khi sync xong / gặp lỗi

## 6. ƯỚC TÍNH SƠ BỘ
- **Độ phức tạp:** Trung bình
- **Rủi ro:**
  - `gkeepapi` là thư viện không chính thức, Google có thể chặn bất cứ lúc nào
  - Master Token cần lấy thủ công, hơi phức tạp cho người mới
  - Google thay đổi API → app có thể ngừng hoạt động

## 7. BƯỚC TIẾP THEO
→ Duyệt Brief → Chạy `/plan` để thiết kế chi tiết → `/code` để implement
