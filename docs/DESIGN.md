# 🎨 DESIGN: GKeepSync (Apple Theme - Light Mode)

Ngày tạo: 2026-03-11
Dựa trên: [PRD.md](PRD.md), [UI_UX.md](UI_UX.md)
Định hướng: Apple Style (MacOS/iOS) - Light Theme, Tối giản, Bo góc mượt mà.

---

## 1. Cách Lưu Thông Tin (Database)

Ứng dụng không sử dụng CSDL phức tạp, tập trung cấu hình file hệ thống:

┌─────────────────────────────────────────────────────────────┐
│  ⚙️ APP CONFIGS (Cài đặt hệ thống - config.json)            │
│  ├── Đường dẫn lưu file .md                                 │
│  ├── Email đăng nhập                                        │
│  ├── Master Token (Bypass login)                            │
│  └── Chu kỳ Auto-sync (15p, 30p...)                        │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  📝 NOTE STATE (Quản lý trạng thái file)                    │
│  ├── ID Ghi chú (Từ Google Keep)                            │
│  ├── Thời gian sửa lần cuối (Tránh ghi đè file cũ)          │
│  └── Trạng thái đồng bộ NotebookLM                          │
└─────────────────────────────────────────────────────────────┘

## 2. Danh Sách Màn Hình (Apple Light Theme)
Sử dụng CustomTkinter, cấu hình `set_appearance_mode("light")` mặc định.

| # | Tên | Trực quan (Apple Light Style) | Mục đích |
|---|-----|------------------------------|----------|
| 1 | **Login Window** | Nền trắng muốt/chữ đen. Rounded Inputs giống màn hình iCloud login. Nút Action màu xanh Blue MacOS. | Xác thực an toàn. |
| 2 | **Sidebar (Cột trái)** | Nền xám rất sáng (Light Gray/Gray95) kiểu mờ. Chữ xám đậm. Menu item bo góc nhỏ khi Hover/Active. | Điều hướng, Filter. |
| 3 | **Content (Cột phải)**| Nền Trắng tinh (White). Các Note Items bo góc `radius=12`, có đổ bóng đổ (drop shadow) hoặc viền mỏng 1px gray. | Hiển thị danh sách Ghi chú. |
| 4 | **Settings Popup** | Giao diện System Settings của MacOS, các khối Cài đặt gộp thành Box (Card), kèm nút Switch bật/tắt tròn trĩnh. | Tùy chỉnh App. |

### 2.1. Chi tiết Màn hình Đăng nhập (Login Window)
**Giao diện & Thành phần (Apple Light / iCloud Style):**
- **Nền (Background):** Trắng tinh.
- **Tiêu đề (Header):** Text "GKeepSync" tối giản, size lớn, chữ đen nhám.
- **Ô nhập liệu (Inputs):** `corner_radius=12`, nền xám cực nhạt (`#F2F2F7`), không viền chướng mắt.
- **Nút bấm chính (Action Button):** Apple Blue (`#007AFF`), chữ trắng in đậm, `corner_radius=12`.
- **Nút/Tab phụ:** Text màu nhạt hoặc xám, không có hộp nổi.

**Test Cases (SDD Compliance - Login):**
- **TC-01: Happy Path:**
  - Given: Mở app chưa có token.
  - When: Nhập email, token đúng -> Bấm Kết nối.
  - Then: Nút xoay loading -> Chuyển sang MainFrame thành công.
- **TC-02: Bỏ trống (Validation):**
  - Given: Form Login.
  - When: Bỏ trống ô email hoặc token -> Bấm Kết nối.
  - Then: Hiện lỗi đỏ nhẹ nhàng "Vui lòng nhập Email / Master Token".
- **TC-03: Trạng thái Loading (UI UX):**
  - Given: Đang tiến hành kết nối.
  - When: Bấm "Kết nối".
  - Then: Nút khóa lại (disabled), không cho spam click, text đổi thành "⏳ Đang kết nối...".

## 3. Luồng Hoạt Động (User Journey)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 **HÀNH TRÌNH: Trải nghiệm mượt mà vào mỗi sáng**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣ **Mở app:** Bật app lên, hiển thị thẳng giao diện Sáng rạng rỡ (Bypass Login nếu đã lưu Token).
2️⃣ **Giao diện chính:** Sidebar xám nhạt (trái), Danh sách ghi chú trắng tinh (phải).
3️⃣ **Đồng bộ ngầm:** Ở góc/Sidebar có chấm trạng thái (Dot Indicator). 
   - Đang kiểm tra: ⏳ Trạng thái Loading spinner nhẹ.
   - Hoàn tất: 🟢 Chấm xanh rêu (hoặc icon Blue tinh tế). Thanh Notification góc phải bọt lên "Updated".
4️⃣ **Tương tác:** Click vào ghi chú, background Item đổi màu xanh nhạt (Selected State giống Finder).
5️⃣ **Tắt máy:** App tự lưu Note State cực nhanh vào JSON.

## 4. Checklist Kiểm Tra & Acceptance Criteria

### Tính năng: Trải nghiệm UI/UX "Thanh Gọn" (Apple Style)
- [ ] Mặc định bật `light` mode. Bỏ ngay các nút bấm vuông vức, mọi thứ phải bo góc (từ `8` đến `15px`).
- [ ] Sidebar phải dùng màu nền tách biệt nhè nhẹ (Ví dụ White cho content, Gray92 cho Sidebar).
- [ ] Nút Action chính (VD: Đăng nhập) là màu Xanh (Apple Blue), các nút phụ (Hủy/Cài đặt) là text hoặc Icon xám/đen.
- [ ] Phía góc trên bên phải của Content view ưu tiên hiển thị Nút "Sync" hình tròn Minimal thay cho nút text dài ngoằng.
- [ ] Font chữ rạch ròi, đậm nhạt theo size (Ví dụ Header size 20 Bold, Text Info 12 mờ).

### Tính năng: Đồng bộ thông minh
- [ ] Bấm "Sync" không làm đứng ứng dụng (UI Freeze) bằng cách xử lý Threading.
- [ ] Xong luồng tải thì thả Notification trượt ra (Toast/Slide Notification).

---
*Tạo bởi AWF - Design Phase*
