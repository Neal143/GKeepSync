# 🎨 GKeepSync UI/UX Guidelines & Document

**Ngày cập nhật:** 2026-03-11

---

## 1. TỔNG QUAN GIAO DIỆN (UI OVERVIEW)

- **Framework sử dụng:** CustomTkinter.
- **Theme chủ đạo:** `dark` (Nền tối).
- **Color Theme định vị:** `blue` (Sắc xanh lam làm điểm nhấn - Active buttons, Highlights).
- **Font & Size:** Sử dụng bộ font hệ thống với các Hierarchy rõ ràng (v.d: H1 = bold 20, Body = normal 13).
- **Kích thước Window:** Mặc định `900x650`, tối thiểu `750x550`.

## 2. KIẾN TRÚC LAYOUT (LAYOUT ARCHITECTURE)

Giao diện được chia theo dạng 2 cột (Sidebar Layout):

### 2.1. Cột trái (Sidebar Navigation)
- Tiêu đề App: GKeepSync (Size 20, Bold).
- **Khối Navigation:**
  - `🏠 Trang chủ`: Nơi cấu hình thư mục, Auto-sync, Hiển thị File Folder.
  - `📝 Google Keep`: Hiển thị danh sách Ghi chú, Lọc theo Tag và Date.
  - `📓 NotebookLM`: Quản lý luồng tích hợp NotebookLM (Đăng nhập, Chọn sổ tay).
  - `⏱️ Lịch sử Sync`: Xem log toàn bộ quá trình đồng bộ (Thành công/Lỗi).
- **Khối Hành động (Actions):**
  - Chức năng Sync tức thời: `🔄 Sync Now` (Vị trí tiện lợi vĩnh viễn ở Sidebar).
  - Nút Logout (`#e74c3c` Đỏ để cảnh báo).

### 2.2. Cột phải (Main Content View)
View nội dung thay đổi theo Sidebar selection.
Chứa các thành phần con với Corner Radius bo tròn, phân cách ranh giới UI bằng các dải màu xám đa tầng (Ví dụ: nền thẻ `gray90` (light) hoặc `gray15` (dark)).

## 3. TRẢI NGHIỆM NGƯỜI DÙNG (UX FLOW)

### 3.1. Luồng Onboarding & Đăng nhập
1. Hiển thị Màn hình Đăng nhập (LoginFrame).
2. Người dùng nhập Email và Master Token/App Password. Nếu có Chrome Extension, sử dụng luồng uỷ quyền tự động vào Localhost Server.
3. Ứng dụng phản hồi (Loading state), Toast Message bật ra.
4. Chuyển vào Trang chủ nếu thành công. Ứng dụng tự đọc credentials saved trong config để Bypass đăng nhập ở lần tiếp theo.

### 3.2. Cấu hình ban đầu
- Trải nghiệm 1 click vào nút "Chọn Thư Mục" mở Context Dialog gốc của hệ điều hành.
- Phản hồi trực quan hiển thị ngay đường dẫn mới.

### 3.3. Luồng Đồng bộ (Sync)
1. User nhấn `Sync Now`.
2. Nút bấm bị khoá (Disabled) kèm text "⏳ Đang sync...", tránh việc spam click.
3. Progress bar tại màn "Lịch sử Sync" thể hiện tiến độ (x/y notes).
4. Notification Toast trôi xuống từ đỉnh màn hình với màu Xanh (Thành công) hoặc Đỏ (Lỗi).
5. Nút bấm trở về trạng thái "🔄 Sync Now", StatusBar chân trang cập nhật thời gian Last Sync.

### 3.4. Duyệt Ghi chú (Keep View)
- List render theo Grid 3 cột (Cho trải nghiệm Grid dạng Card tương tự Google Keep gốc).
- Filter Tag & Date tự động fetch Database local hoặc State In-Memory thay vì query trực tiếp lên server Google Keep liên tục để tăng tốc độ phản hồi.
- Nếu Card rỗng → Hiện text Placeholder "Không tìm thấy ghi chú nào".

## 4. COMPONENT ĐỊNH CHUẨN

- **Cards:** Bo góc `corner_radius=8`. Padding trong `padx=12, pady=12`. Chứa Tiêu đề đậm (bold), Snippet mờ (gray text), Meta footer (Tags).
- **Inputs & Dropdowns:** Đồng nhất Style theo CustomTkinter mặc định Theming. Chiều cao tiêu chuẩn thao tác.
- **Log / History Terminal:** Sử dụng ScrollableFrame, phân loại log theo màu sắc font: Xanh lá (Success), Đỏ (Error), Trắng/Xám (Info).
- **Notification Toast:** Toast component tự nổi lên ở tọa độ `relx=0.5, rely=0.02` và biến mất sau 4 giây.
