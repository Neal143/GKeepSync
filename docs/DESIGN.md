# 🎨 DESIGN: GKeepSync (Google Material 3 - Light Theme)

Ngày tạo: 2026-03-11
Dựa trên: [PRD.md](PRD.md), [UI_UX.md](UI_UX.md)
Định hướng: Google Material 3 - Light Theme, Thẻ nổi đa chiều (Cards), Bóng đổ mượt mà (Shadows).

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

## 2. Danh Sách Màn Hình (Material 3 Light Theme)
Sử dụng CustomTkinter, cấu hình `set_appearance_mode("light")` mặc định.

| # | Tên | Trực quan (Material 3 Style) | Mục đích |
|---|-----|------------------------------|----------|
| 1 | **Login Window** | Nền trắng nhạt. Form Login được chứa trong 1 Card lớn có đổ bóng, Input fields nổi khối tinh tế, Nút Action tròn trịa. | Xác thực an toàn. |
| 2 | **Sidebar (Cột trái)** | Nền trắng (`#FFFFFF`). Đổ bóng (box-shadow) dâng lên tách biệt rõ khỏi vùng nội dung bên phải. Nút "Sync Now" nổi bật. | Điều hướng, Lọc, Đồng bộ. |
| 3 | **Content (Cột phải)**| Nền Xám rất nhạt (`#F5F5F7` hoặc `gray95`). Các Note Items hoặc Settings bọc trong Card góc bo `radius=12`, đổ bóng êm. | Hiển thị thông tin chính. |
| 4 | **Settings Popup** | Giao diện Card-based. Các khối Cài đặt gộp thành Box (Card), nút Switch tròn theo chuẩn Material. | Tùy chỉnh App. |
| 5 | **NotebookLM Tab** | Trạng thái rỗng: Hero Card có nút gọi hành động lớn. Trạng thái kết nối: Grid hiển thị các Sổ tay (Notebooks) dạng Card nổi, viền xanh (active). | Quản lý đồng bộ NotebookLM. |

### 2.1. Chi tiết Màn hình Đăng nhập (Login Window)
**Giao diện & Thành phần (Material 3 Style):**
- **Nền (Background):** Xám nhạt (`#F5F5F7`).
- **Khung chứa Form:** Là một Card lớn màu trắng (`#FFFFFF`), bo góc bự (ví dụ 16px), đổ bóng Drop Shadow.
- **Tiêu đề (Header):** Text "GKeepSync" rõ ràng, chữ đen nhám.
- **Ô nhập liệu (Inputs):** Dạng thẻ nổi (Embedded Material Look).
- **Nút bấm chính (Action Button):** Màu Xanh đậm, bo góc tròn viên thuốc (pill shape).

**Test Cases (SDD Compliance - Login):**
- **TC-01: Happy Path:**
  - Given: Mở app chưa có token.
  - When: Nhập email, token đúng -> Bấm Kết nối.
  - Then: Nút xoay loading -> Chuyển sang MainFrame thành công.
- **TC-02: Bỏ trống (Validation):**
  - Given: Form Login.
  - When: Bỏ trống ô email hoặc token -> Bấm Kết nối.
  - Then: Hiện lỗi đỏ dạng Toast/Label: "Vui lòng nhập Email / Master Token".
- **TC-03: Trạng thái Loading (UI UX):**
  - Given: Đang tiến hành kết nối.
  - When: Bấm "Kết nối".
  - Then: Nút khóa lại (disabled), không cho spam click, text đổi thành "⏳ Đang kết nối...".

### 2.2. Chi tiết Trang chủ (Dashboard & Settings)
**Giao diện & Thành phần:**
- **Sidebar (Trái):** Nền trắng (`#FFFFFF`), có bóng đổ (box-shadow) nhẹ sang phải để tách biệt với vùng nội dung. Chứa Logo, các Menu điều hướng và nút "Sync Now" nổi bật ở viền dưới.
- **Vùng nội dung (Phải):** Nền xám nhạt (`#F5F5F7` hoặc `gray95`). Chứa các khối Cài đặt (Chọn thư mục, Auto-sync).
- **Cards Settings:** Mỗi mục cài đặt nằm trong một thẻ (Card) nền trắng, bo tròn 12px, có bóng đổ êm mượt. Các nút Switch bật/tắt mang phong cách Material 3 (tròn trịa, màu trạng thái rõ ràng).

**Test Cases (Dashboard):**
- **TC-04: Cấp bậc thị giác (Visual Hierarchy):**
  - Given: Đang ở màn hình Trang chủ.
  - When: Quan sát bố cục Sidebar và Main Content.
  - Then: Sidebar (trắng) phân tách rõ ràng với Main Content (xám nhạt) thông qua bóng đổ, tạo cảm giác phân tầng (đa chiều).
- **TC-05: Cài đặt dạng Thẻ (Card-based Settings):**
  - Given: Đang ở màn hình Cài đặt (Trang chủ).
  - When: Thao tác chọn thay đổi Thư mục lưu trữ.
  - Then: Toàn bộ form và thông tin được gói gọn, bo tròn gọn gàng trong 1 panel màu trắng nổi lên trên nền xám. Phản hồi chọn file mượt mà.

### 2.3. Chi tiết Quản lý Ghi chú (Google Keep View)
**Giao diện & Thành phần:**
- **Bố cục (Layout):** Render dưới dạng lưới (Grid) 3-4 cột tương tự giao diện Google Keep hoặc Pinterest.
- **Thẻ Ghi chú (Note Card):** Background trắng (`#FFFFFF`), `corner_radius=12`, đổ bóng Drop Shadow. Tiêu đề in đậm, trích dẫn nội dung xám nhạt (`Text Muted`).
- **Tag Indicator:** Các thẻ nhãn dán nằm ở mép dưới của Note Card, dạng hình "viên thuốc" (pill shape), nền pastel nhẹ nhàng (ví dụ: lục nhạt, lam nhạt).

**Test Cases (Keep View):**
- **TC-06: Grid Alignment & Card Styling:**
  - Given: Đã có sẵn 10 ghi chú và chuyển sang tab "Google Keep".
  - When: Danh sách được nạp/hiển thị.
  - Then: Render đúng cấu trúc Lưới (Grid). Mỗi ghi chú nằm gọn trong Card bo góc 12px, bóng đổ rõ nét, không bị tràn (overflow) text.
- **TC-07: Tương tác Hover (Micro-interactions):**
  - Given: Đưa chuột (hover) vào một thẻ ghi chú bất kỳ.
  - When: Chuột lướt qua Note Card.
  - Then: Bóng đổ đậm/lớn hơn hoặc thẻ hơi nẩy lên (scale) để báo hiệu đang focus, viền thẻ (nếu có) đổi màu xanh Primary mờ.

### 2.4. Chi tiết Lịch sử Đồng bộ (Sync Log Frame)
**Giao diện & Thành phần:**
- **Khung chứa Log:** Mô phỏng dạng Terminal thu nhỏ gắn trong một Thẻ Card to (Trắng).
- **Màu nền Terminal:** Đen mờ hoặc Terminal Xám Sáng (`Gray90`).
- **Typography:** Font Code (ví dụ: `Consolas` hoặc `Courier New`) để dễ đọc mã Status/Error. Phân cấp màu (Đỏ = Lỗi, Xanh = Thành công, Xám = Info).

**Test Cases (Sync Log):**
- **TC-08: Format Log chuẩn Material:**
  - Given: Màn hình Sync Log.
  - When: Có log mới bắn về.
  - Then: Log cuộn mượt (Scrollable), chữ dạng Code nằm lọt thỏm đẹp đẽ trong Card bo góc, màu sắc phân định trạng thái rõ rệt.
- **TC-09: Animation Toast Đồng bộ:**
  - Given: Đang làm việc ở tab bất kỳ, user bấm nút 'Sync Now' trên Sidebar.
  - When: Đồng bộ hoàn tất thành công.
  - Then: Thông báo Toast Toast Notification hiển thị dưới dạng thẻ Card nhỏ từ đỉnh rớt xuống báo "✅ Hoàn tất", tự biến mất sau vài giây. Nút Sync Now khôi phục trạng thái cũ.

### 2.5. Chi tiết Tích hợp NotebookLM (NotebookLM Integration)
**Giao diện & Thành phần:**
- **Trạng thái Chưa Đăng Nhập:** Nằm căn giữa màn hình là một Card lớn (Hero Card) chứa Logo/Icon NotebookLM, dòng mô tả tính năng mượt mà (`Text Muted`), kèm nút "Kết nối NotebookLM" nằm nổi khối.
- **Trạng thái Đã Kết Nối:** Nửa trên là Card Profile (Email, Nút Disconnect nằm góc, bo tròn nhạt). Nửa dưới hiển thị danh sách các "Sổ tay" (Notebooks) dạng Lưới (Grid) các Card nhỏ.
- **Sổ tay Card (Notebook Card):** Một thẻ Trắng bo góc (`radius=12px`). Click vào sẽ lún nhẹ và viền ngoài chớp sáng lên màu viền Primary (Ví dụ Xanh dương) báo hiệu rằng Sổ tay này đã được Active làm nguồn đồng bộ.

**Test Cases (NotebookLM):**
- **TC-10: Giao diện Empty State NotebookLM:**
  - Given: User chưa kết nối với NotebookLM CLI.
  - When: Click vào tab NotebookLM ở Sidebar.
  - Then: Render Form kết nối dạng Card lớn, bo góc 16px giữa màn hình xám nhạt, có đổ bóng mạnh lấy chiều sâu.
- **TC-11: Hiệu ứng Chọn Sổ tay (Visual Selection):**
  - Given: Render Grid 5 quyển sổ tay (Notebooks).
  - When: User click vào thiết lập quyển A làm mặc định.
  - Then: Viền Card quyển A phát sáng/hiển thị rõ viền Primary mượt mà, bóng đổ dày lên (Pop up effect), đồng thời các Card khác mờ nhẹ.


## 3. Luồng Hoạt Động (User Journey)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 **HÀNH TRÌNH 1: Nhấn Đồng Bộ (Sync Now)**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣ Đang làm việc → Nhìn sang góc dưới Sidebar.
2️⃣ Bấm nút to nổi bật 🔄 **Sync Now** (Nút có màu Xanh Primary, khi hover sẽ nổi bóng lên).
3️⃣ Nút mờ đi (Loading), thanh Progress Bar ở cạnh dưới chạy.
4️⃣ Đồng bộ xong → Một "Toast" (Thẻ thông báo nhỏ) màu Xanh rớt nhẹ từ trên đầu màn hình xuống: "✅ Đã đồng bộ 25 ghi chú!".
5️⃣ Nút Sync Now sáng lên lại, sẵn sàng.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 **HÀNH TRÌNH 2: Tìm Note trên App**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣ Bấm tab 'Google Keep' bên Sidebar.
2️⃣ Màn hình chính hiện hàng loạt Thẻ Note (Cards).
3️⃣ Bấm vào 1 thẻ Tag (VD: #work) ở góc trên → Lưới thẻ tự mượt mà lọc lại chỉ còn Note chứa Tag đó.

## 4. Checklist Kiểm Tra & Acceptance Criteria

### Tính năng: Trải nghiệm UI/UX Thẻ Nổi (Material 3)
- [ ] Mặc định bật `light` mode. Mọi phần giao diện đều bọc trong Card màu Trắng.
- [ ] Sidebar Trắng (Đổ bóng phải), Content xám (`gray95`). Phân biệt trực quan rõ.
- [ ] Nút Action chính là màu Xanh, bo góc như viên thuốc, có hover nhẹ nhàng nổi lên.
- [ ] Font chữ rõ ràng, phân cấp Hierarchy (14px, 16px, 20px).

### Tính năng: Đồng bộ thông minh
- [ ] Bấm "Sync" phải báo Loading trong suốt luồng tiến trình thao tác.
- [ ] Xong luồng tải thì thả Notification trượt ra êm mượt.

## 5. 🖼️ MOCKUPS (Material 3 Drafts)

### 5.1. Màn hình Login (Login Window) - Tách biệt 2 Luồng Flow
**Màn hình 1: Giao diện Kết nối qua Trình Duyệt (Mặc định)**
![Login Browser Material 3 Mockup](/C:/Users/ADMIN/.gemini/antigravity/brain/e7782ae8-48ed-49a2-bda5-a9c24b94e435/gkeepsync_login_browser_material3_light_1773239077140.png)

**Màn hình 2: Giao diện Nhập mã Thủ công (Chuyển đổi)**
![Login Manual Material 3 Mockup](/C:/Users/ADMIN/.gemini/antigravity/brain/e7782ae8-48ed-49a2-bda5-a9c24b94e435/gkeepsync_login_manual_material3_light_1773239132231.png)

### 5.2. Trang Chủ (Dashboard)
![Dashboard HomeView Material 3 Mockup](/C:/Users/ADMIN/.gemini/antigravity/brain/e7782ae8-48ed-49a2-bda5-a9c24b94e435/gkeepsync_dashboard_v4_material3_light_1773241167309.png)

### 5.3. Quản Lý Ghi Chú (Google Keep View)
![Notes Grid Material 3 Mockup](/C:/Users/ADMIN/.gemini/antigravity/brain/e7782ae8-48ed-49a2-bda5-a9c24b94e435/gkeepsync_keepview_material3_light_1773225259389.png)

### 5.4. Tích hợp NotebookLM (NotebookLM Integration)
![NotebookLM Integration Material 3 Mockup](/C:/Users/ADMIN/.gemini/antigravity/brain/e7782ae8-48ed-49a2-bda5-a9c24b94e435/gkeepsync_notebooklm_material3_light_1773225296810.png)

### 5.5. Lịch sử Đồng bộ (Sync Log Frame)
![Sync Log Terminal Material 3 Mockup](/C:/Users/ADMIN/.gemini/antigravity/brain/e7782ae8-48ed-49a2-bda5-a9c24b94e435/gkeepsync_synclog_material3_light_1773225276602.png)

---

## 6. Kiến Trúc Module (Sau Refactor - 2026-03-14)

Sau quá trình Refactor 2 giai đoạn, code base được tổ chức theo nguyên tắc **Single Responsibility Principle (SRP)**:

### 6.1. Sơ đồ phân tầng trách nhiệm

```
app.py (GKeepSyncApp)           ← Orchestrator: Login, Auto-sync, NLM Worker
│   └── ui/tray_manager.py      ← System Tray lifecycle (pystray + PIL)
│
└── ui/main_frame.py            ← Router: Routing data → Views [KHÔNG VẼ UI]
    ├── ui/views/home_view.py   ← Trang chủ: Settings, Auto-sync switch, Startup toggle
    ├── ui/views/keep_view.py   ← Google Keep: Vẽ lưới Apple Cards, render ghi chú
    ├── ui/views/nlm_view.py    ← NotebookLM: Vẽ danh sách Notebooks và Sources
    └── ui/views/sync_view.py   ← Lịch sử Sync: Vẽ Log Terminal (Keep + NLM)
```

### 6.2. Phân chia trách nhiệm

| Module | Trách nhiệm duy nhất |
|---|---|
| `app.py` | Khởi tạo app, quản lý Login, điều phối Sync, NLM background thread |
| `ui/tray_manager.py` | Toàn bộ lifecycle của System Tray Icon |
| `ui/main_frame.py` | Định tuyến Data từ `app.py` → View con (chỉ Forward, KHÔNG Render) |
| `ui/views/keep_view.py` | Tự vẽ lưới 4 cột Note Cards (`render_notes()`) |
| `ui/views/nlm_view.py` | Tự vẽ danh sách Notebooks (`set_nlm_notebooks()`) và Sources (`set_nlm_sources()`) |
| `ui/views/sync_view.py` | Tự ghi Log Terminal (`append_keep_log()`, `append_nlm_log()`) |

### 6.3. Cơ chế Startup ngầm

```
Windows bật máy
    → Startup Folder: GKeepSync_Fix.lnk (--start-hidden)
    → app.py.__init__: alpha=0.0 → hide_to_tray()
    → TrayManager tạo Icon ở System Tray
    → App chạy ngầm, Auto-sync theo lịch đã hẹn
```

---
*Tạo bởi AWF - Design Phase | Cập nhật Refactor: 2026-03-14*
