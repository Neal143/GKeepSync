# 💡 Product Requirements Document (PRD): GKeepSync

**Ngày cập nhật:** 2026-03-14
**Hiện trạng:** Version 1.x (Core + NotebookLM + Background Run)
**Loại sản phẩm:** Desktop App (Windows)

---

## 1. MỤC TIÊU SẢN PHẨM (Mục đích cốt lõi)
GKeepSync là ứng dụng Desktop giúp người dùng Google Keep tải và đồng bộ hai chiều (hiện tại là một chiều tải xuống) ghi chú về máy tính dưới định dạng Markdown (.md) để lưu trữ an toàn, tìm kiếm offline và dễ dàng tích hợp vào quy trình làm việc khác (Obsidian, Notion, NotebookLM).

## 2. PHẠM VI TÍNH NĂNG (Features Scope)

### 2.1. Xác thực & Đăng nhập (Authentication)
- **Đăng nhập bằng App Password / Master Token:** Nhập trực tiếp vào App (thông qua `gkeepapi` + `gpsoauth`).
- **Đăng nhập bằng OAuth (Chrome Extension):**
  - **Cơ chế hoạt động:** Giao diện Extension trên trình duyệt có nhiệm vụ mở tab đăng nhập `EmbeddedSetup` của tài khoản Google. Sau khi tải trang thành công, Extension trích xuất phân tích cookie tạm thời `oauth_token` của chính tab đó.
  - Extension ưu tiên tự động gửi `oauth_token` (có hoặc không có Email đi kèm) về **Token Server (Localhost)** đang chạy ngầm của GKeepSync App thông qua HTTP POST.
  - App GKeepSync sẽ nhận `oauth_token`, kết hợp với Email tĩnh mà người dùng đã nhập trên giao diện Desktop (nếu Extension không bắt được Email), và gọi hàm `exchange_oauth_for_master` để đổi lấy **Master Token** chính thức. Cuối cùng, App sẽ **trả ngược Master Token lại cho Extension** thông qua API Response.
  - **Lưu trữ bảo mật dài hạn & Auto-login Extension:** Cả **App GKeepSync** và **Extension** đều lưu lại thông tin Master Token này (`config.json` và `chrome.storage.local`). Nếu token trên trình duyệt còn hợp lệ, luồng Auto-login của Extension sẽ nhảy qua bước `EmbeddedSetup` và tự động gửi thẳng token về phía local server.
- **Dịch vụ Xác thực Lõi (Core Auth Services):** App Desktop sử dụng một Auth Service giúp kiểm tra liên kết `config.json` liên tục trên ổ cứng. Nếu có sẵn Master Token hợp lệ từ lần dùng trước, ứng dụng sẽ Bypass hoàn toàn màn hình Đăng Nhập và vào thẳng Trang Chủ.

### 2.2. Giao diện & Quản lý (Quản trị chung)
- **Cấu hình thư mục lưu trữ:** Cho phép chọn đường dẫn thư mục lưu các file `.md`.
- **Giao diện Sidebar (Navigation):** Chuyển đổi linh hoạt giữa Trang chủ, Google Keep, NotebookLM, Lịch sử Sync.
- **Light Theme:** Giao diện CustomTkinter theo chuẩn Material 3 Light.

### 2.3. Tính năng Đồng bộ Ghi chú (Sync Engine)
- **Đồng bộ thủ công (Manual Sync):** Nút "Sync Now", lấy từ xa và lưu xuống thư mục local.
- **Đồng bộ tự động (Auto Sync):** Lên lịch đồng bộ tự động theo chu kỳ: 15 phút, 30 phút, 60 phút, 3 giờ, 6 giờ chạy ngầm.
- **Xử lý trùng lặp & Cập nhật mới:** So sánh nội dung, chỉ ghi đè file `.md` nếu phát hiện thay đổi. Xử lý trùng lặp Title bằng cách nối thêm ID của Google Keep. Note: Trạng thái đồng bộ được theo dõi độc lập theo từng file (tải từ Keep & đẩy lên NLM) qua RAM-state map hiển thị trên DataGrid (File-Centric Dashboard).

### 2.4. Tính năng Trích lọc (Filters)
- **Lọc theo Nhãn (Tag/Label):** Quản lý đồng bộ hoặc xem trước các danh mục chuyên biệt dựa vào Labels có sẵn trên Keep.
- **Lọc theo Thời gian:** Chọn từ ngày - đến ngày để khoanh vùng đồng bộ.

### 2.5. Tích hợp AI Kiến thức (NotebookLM Integration)
- Đăng nhập phiên tài khoản NotebookLM.
- Tự động fetch danh sách Sổ tay (Notebooks) & Nguồn (Sources).
- **Auto-Upload & Background Sync Worker:** Dịch vụ tích hợp NotebookLM hoạt động dựa trên một luồng Thead ngầm (NLM Background Worker). Sau khi sync ghi chú từ Keep về Local, App sẽ truyền tín hiệu và worker tiến hành tự động đẩy các thay đổi tương ứng lên Notebook được chỉ định nhằm làm giàu nguồn dữ liệu AI, không gây đóng băng (freeze) giao diện người sử dụng.

### 2.6. Chạy ngầm & Khởi động cùng Windows (Background Run)
- **System Tray:** Khi nhấn [X], app không tắt hẳn mà ẩn xuống System Tray (góc dưới màn hình). Menu chuột phải bao gồm: Mở App, Đồng bộ ngay, Thoát hẳn.
- **Windows Startup:** Tính năng "Khởi động cùng Windows" được quản lý qua Startup Folder (`shell:startup`). App sẽ khởi động ngầm (không hiện cửa sổ) khi máy tính bẫt.
- **Ghost Window Prevention:** Thực hiện alpha-trick (`alpha=0.0`) để đảm bảo Tkinter không hiện màn hình trắng trung gian khi khởi động ngầm.

## 3. CÔNG NGHỆ SỬ DỤNG
- **Ngôn ngữ:** Python 3.x
- **Giao diện:** CustomTkinter (UI Grid/Frame modularized, Material 3 Light Theme)
- **API Core:** `gkeepapi`, `gpsoauth`
- **System Tray:** `pystray`, `Pillow (PIL)`
- **Đóng gói dự án:** PyInstaller (`.spec` builder)

## 4. RỦI RO CHIẾN LƯỢC CẦN KIỂM SOÁT
- Cập nhật Google API làm hỏng luồng hoạt động của `gkeepapi`.
- Đăng nhập gián tiếp thông qua Extension rủi ro bị thay đổi chính sách từ Chrome Web Store.
- NotebookLM API hiện tại đang sử dụng worker, có thể thay đổi policy của dịch vụ.
