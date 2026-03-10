# 🗺️ Bản Đồ Theo Dõi Thành Phần Giao Diện (UI Mapping)

**Dự án:** GKeepSync
**Ngày tạo:** 2026-03-11
**Mục đích:** Tài liệu này liệt kê toàn bộ các thành phần hiển thị trên giao diện (Buttons, Labels, Inputs, Frames, Switch, OptionMenus) cùng với **Tên biến trong hệ thống (Variable / Component Name)**. Khi chúng ta trao đổi, hãy sử dụng các tên này để đảm bảo độ chính xác khi can thiệp vào mã nguồn.

---

## 1. Màn Hình Đăng Nhập (LoginFrame)
*File: `ui/login_frame.py`*

### 1.1. Tab 1: Đăng nhập qua Browser
| Tên hiển thị trên UI | Loại Component | Tên biến trong code |
|----------------------|----------------|---------------------|
| Khung Tab "🌐 Đăng nhập qua Browser" | CTkTabview Tab | `tab_browser` |
| Textbox nhập Email | CTkEntry | `self._browser_email` |
| Nút "1️⃣ Mở trình duyệt đăng nhập" | CTkButton | `self._open_browser_btn` |
| Textbox nhập oauth_token | CTkEntry | `self._oauth_entry` |
| Nút "3️⃣ Lấy Master Token & Kết nối" | CTkButton | `self._browser_connect_btn` |

### 1.2. Tab 2: Nhập Master Token (Thủ công)
| Tên hiển thị trên UI | Loại Component | Tên biến trong code |
|----------------------|----------------|---------------------|
| Khung Tab "🔑 Nhập Master Token" | CTkTabview Tab | `tab_manual` |
| Textbox nhập Email | CTkEntry | `self._email_entry` |
| Textbox nhập Master Token | CTkEntry | `self._token_entry` |
| Checkbox "Hiện token" | CTkCheckBox | `self._show_token` |
| Nút "🔗 Kết nối" | CTkButton | `self._connect_btn` |

### 1.3. Thành phần chung Login
| Tên hiển thị trên UI | Loại Component | Tên biến trong code |
|----------------------|----------------|---------------------|
| Khung chọn Tab | CTkTabview | `self._tabview` |
| Dòng trạng thái (Báo lỗi/thành công) | CTkLabel | `self._status_label` |

---

## 2. Menu Điều Hướng Chính (Sidebar in MainFrame)
*File: `ui/main_frame.py`*

| Tên hiển thị trên UI | Loại Component | Tên biến trong code |
|----------------------|----------------|---------------------|
| Màn hình chính | CTkFrame | `MainFrame` |
| Thanh Sidebar | CTkFrame | `self._sidebar` |
| Nút Navigation "🏠 Trang chủ" | CTkButton | `self._home_btn` |
| Nút Navigation "📝 Google Keep" | CTkButton | `self._keep_btn` |
| Nút Navigation "📓 NotebookLM" | CTkButton | `self._nlm_btn` |
| Nút Navigation "⏱️ Lịch sử Sync" | CTkButton | `self._sync_btn_nav` |
| Nút Hành động "🔄 Sync Now" | CTkButton | `self._sync_btn` |
| Nút "Đăng xuất" (Màu đỏ) | CTkButton | `self._logout_btn` |

---

## 3. Khung Nhìn Trang Chủ (HomeView)
*File: `ui/views/home_view.py`*

| Tên hiển thị trên UI | Loại Component | Tên biến trong code |
|----------------------|----------------|---------------------|
| Textbox đường dẫn Thư mục | CTkEntry | `self._folder_entry` (linked `folder_var`) |
| Nút "Browse" (Chọn thư mục) | CTkButton | (Nút Browse không lưu biến, chỉ trigger event) |
| Dropdown "⏰ Auto Sync" (Chu kỳ) | CTkOptionMenu | `self._interval_dropdown` (linked `interval_var`) |
| Công tắc bật/tắt Auto Sync | CTkSwitch | `self._auto_sync_switch` |
| Thanh Status Bar dưới cùng | StatusBar | `self.status_bar` |
| Text Trạng thái kết nối (Bên trái Status) | CTkLabel | `self._status_label` (trong StatusBar) |
| Text Lịch sử Sync (Bên phải Status) | CTkLabel | `self._sync_label` (trong StatusBar) |

---

## 4. Khung Nhìn Google Keep (KeepView)
*File: `ui/views/keep_view.py`*

| Tên hiển thị trên UI | Loại Component | Tên biến trong code |
|----------------------|----------------|---------------------|
| Dropdown Chọn "🏷️ Tag" | CTkOptionMenu | `self.tag_dropdown` (linked `tag_var`) |
| DatePicker "📅 Từ" | DateEntry | `self.date_from` |
| DatePicker "Đến" | DateEntry | `self.date_to` |
| Text đếm số note ("x notes") | CTkLabel | `self.note_count_label` |
| Vùng cuộn danh sách Ghi chú | CTkScrollableFrame | `self.notes_scroll` |

**(Mỗi thẻ Ghi chú Note Card sinh ra động sẽ chứa các Labels cơ bản: Tiêu đề, Nội dung Preview, Labels text, Date text)**

---

## 5. Khung Nhìn NotebookLM (NLMView)
*File: `ui/views/nlm_view.py`*

| Tên hiển thị trên UI | Loại Component | Tên biến trong code |
|----------------------|----------------|---------------------|
| Công tắc Sync NotebookLM | CTkSwitch | `self.nlm_switch` |
| Textbox nhập Notebook ID | CTkEntry | `self.nlm_id_entry` (linked `nlm_id_var`) |
| Nút "Đăng nhập NLM" | CTkButton | `self.nlm_login_btn` |
| Nút "Tải Notebooks" | CTkButton | `self.fetch_nb_btn` |
| Vùng cuộn danh sách "📚 My Notebooks" | CTkScrollableFrame | `self.nb_scroll` |
| Vùng cuộn danh sách "📄 Sources" | CTkScrollableFrame | `self.src_scroll` |

---

## 6. Khung Nhìn Lịch Sử Sync (SyncView)
*File: `ui/views/sync_view.py`*

| Tên hiển thị trên UI | Loại Component | Tên biến trong code |
|----------------------|----------------|---------------------|
| Thanh Progress Bar hiển thị | SyncProgressBar | `self.progress` |
| Vùng cuộn "📝 Google Keep Log" | CTkScrollableFrame | `self.keep_log_scroll` |
| Vùng cuộn "📓 NotebookLM Log" | CTkScrollableFrame | `self.nlm_log_scroll` |

---

## 7. Các Global Overlays (Components chung)
*File: `ui/components.py`*

| Tên hiển thị trên UI | Loại Component | Tên biến trong hệ thống (Class name) |
|----------------------|----------------|--------------------------------------|
| Khung Nhập Chữ/Ngày | CTkFrame bọc Entry | `DateEntry` |
| Thanh Trạng thái dòng dưới | CTkFrame bọc Labels | `StatusBar` |
| Thông báo nổi (Toast nổi lên 4s) | CTkFrame bọc icon/text | `NotificationToast` |
| Khung Progress Bar | CTkFrame bọc CTkProgressBar| `SyncProgressBar` |

---
**💡 Tips giao tiếp với AI:**
Nếu anh muốn sửa gì, chỉ cần nhắn ví dụ: *"Thay màu chữ của self._sync_btn sang xanh"* hoặc *"Thêm một nút kế bên self.fetch_nb_btn trong NLMView"*. Em sẽ tìm chính xác và sửa ngay lập tức!

---

## 8. Chrome Extension Cũ (Popup)
*Vị trí file cũ: `extension cũ/popup.html`*

| Tên hiển thị trên UI | Loại Component (HTML) | Tên biến / ID (DOM) |
|----------------------|-----------------------|---------------------|
| Dòng trạng thái (Status) | `<div>` | `id="status"` |
| Nút "🌐 Đăng nhập Google" | `<button>` | `id="loginBtn"` |
| Textbox nhập Email | `<input>` | `id="emailInput"` |
| Textbox nhập Token | `<input>` | `id="tokenInput"` |
| Nút "🚀 Gửi Token đến App GKeepSync" | `<button>` | `id="sendBtn"` |
