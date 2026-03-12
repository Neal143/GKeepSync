# 🎨 GKeepSync UI/UX Guidelines & Component System (Material 3)

**Ngày cập nhật:** 2026-03-11

Tài liệu quy chuẩn thiết kế UI/UX theo phong cách **Google Material 3 (Light Theme)** dành riêng cho ứng dụng Desktop GKeepSync sử dụng framework CustomTkinter.

---

## 1. THIẾT KẾ ĐẠI CƯƠNG (DESIGN TOKENS)

### 1.1. Bảng Màu (Color Palette)
- **Nền chính (Background):**
  - Main Window (Sidebar): Trắng `#FFFFFF`
  - Vùng nội dung (Content Area): Xám nhạt `#F5F5F7` hoặc `gray95`
- **Màu nhấn (Primary/Accent):**
  - Xanh Dương Đậm (Google Blue): `#1A73E8` - Dùng cho nút Action chính, Checkbox active.
  - Xanh Dương Nhạt (Hover/Focus): `#E8F0FE` - Dùng khi di chuột vào sidebar item hoặc bôi đen.
- **Màu hỗ trợ (Semantic Colors):**
  - Lỗi (Error/Danger): Đỏ `#EA4335` (Nút Logout, Text báo lỗi, Toast thất bại)
  - Thành công (Success): Xanh lá `#34A853` (Toast đồng bộ xong, Status hoạt động)
  - Cảnh báo (Warning): Vàng `#FBBC04`
- **Typography & Font Colors:**
  - Tiêu đề (Headings): Đen `#1F1F1F` hoặc `#000000` (Font size: 18 - 24, Bold)
  - Text thường (Body): Xám đậm `#4A4A4A` (Font size: 13 - 14, Normal)
  - Text phụ/Mờ (Muted/Placeholder): Xám nhạt `#757575` (Font size: 12)

### 1.2. Khoảng cách & Bo góc (Spacing & Layout Elements)
- **Kích thước Window:** Mặc định `900x650`, tối thiểu `750x550`.
- **Bo góc (Border Radius):**
  - Vùng Card lớn, Box chứa cài đặt: `corner_radius = 12px` hoặc `16px`.
  - Nút bấm (Buttons) và Input text: `corner_radius = 8px`.
  - Badge, Tags: Viên thuốc `pill` (bo tròn hoàn toàn hai đầu, corner_radius bằng nửa chiều cao).
- **Khoảng cách (Padding/Margin):**
  - Padding trong lõi Card: `padx=16`, `pady=16`.
  - Khoảng trống giữa các Block: `10px` đến `20px`.
- **Mô phỏng Đổ bóng (Shadows):**
  - Do hạn chế của CustomTkinter, ta tạo cảm giác các khối nổi lên bằng cách đặt Frame nền trắng tinh `#FFFFFF` trồi lên giữa Frame màu nền xám nhạt `#F5F5F7` đi kèm với một đường viền `border_color="#E0E0E0"`, `border_width=1` cực kỳ tinh tế.

---

## 2. QUY CHUẨN THÀNH PHẦN (COMPONENT GUIDELINES)

### 2.1. Nút Bấm (Button System)
- **Primary Button (Nút Hành Động Chính):**
  - *Áp dụng:* Nút "🔄 Sync Now", "Kết nối", "Đăng nhập".
  - *Style:* `fg_color="#1A73E8"`, `text_color="#FFFFFF"`, `hover_color="#1557A0"`, `corner_radius=8`.
  - *Disabled State:* Màu nền bợt đi `#E0E0E0`, chữ `#A8A8A8`.
- **Secondary Button (Nút Phụ):**
  - *Áp dụng:* Nút Browse thư mục, Nút Hủy (Cancel).
  - *Style:* `fg_color="#F1F3F4"` (hoặc `transparent`), `text_color="#1A73E8"`, `hover_color="#E8F0FE"`.
- **Outline Button (Nút Viền):**
  - Dùng thứ cấp khi không muốn tốn diện tích chú ý. Nền màu trong suốt, viền xanh `#1A73E8`, chữ `#1A73E8`.
- **Danger Button (Nút Nguy Hiểm):**
  - *Áp dụng:* Logout, Xóa Cache.
  - *Style:* `fg_color="#EA4335"`, hover sang màu đỏ đậm hơn.

### 2.2. Nhập Liệu & Lựa Chọn (Inputs & Toggles)
- **Text Entry / Password:**
  - Nền viền (border): `#DADCE0`, nền ô (bg_color): `#FFFFFF`.
  - Khi gõ (Focus): Cần xử lý nổi bật bằng đường viền xanh (`border_color="#1A73E8"`).
- **Switch (Công tắc Bật/Tắt):**
  - Active: Trượt màu Xanh `#1A73E8`. Inactive: Cục trượt Xám Nhạt `#DADCE0`.
- **OptionMenu / Dropdown:**
  - Trông giống nút Secondary. Nền `#F1F3F4`, mũi tên chĩa xuống quen thuộc.

### 2.3. Dạng Thẻ (Card System)
- **Card Nội dung tĩnh (Cài đặt, Profile):** Một Frame màu trắng góc bo 12px.
- **Note Card (Thẻ Google Keep):** 
  - Render theo Grid. Card trắng bo 12px. 
  - Khi chuột Hover: Có thể đổi nhẹ màu nền sang `#F8F9FA` hoặc viền xanh để thể hiện tính tương tác.
- **Log Terminal (Sync Log):** 
  - Màn hình mô phỏng dòng lệnh dạng ScrollableFrame nền xám đậm `gray15` và font Monospace (Consolas) để tách biệt không gian đọc dữ liệu gỡ lỗi trực quan nhạy cảm.

---

## 3. KIẾN TRÚC LAYOUT (LAYOUT ARCHITECTURE)

Giao diện được chia theo dạng 2 cột (Sidebar Layout):

### 3.1. Cột trái (Sidebar Navigation)
- Tiêu đề App: GKeepSync (Size 20, Bold).
- **Khối Navigation:**
  - `🏠 Trang chủ`: Nơi cấu hình thư mục, Auto-sync, Hiển thị File Folder.
  - `📝 Google Keep`: Hiển thị danh sách Ghi chú, Lọc theo Tag và Date.
  - `📓 NotebookLM`: Quản lý luồng tích hợp NotebookLM (Đăng nhập, Chọn sổ tay).
  - `⏱️ Lịch sử Sync`: Xem log toàn bộ quá trình đồng bộ (Thành công/Lỗi).
- **Khối Hành động (Actions):**
  - Chức năng Sync tức thời: `🔄 Sync Now` (Vị trí tiện lợi vĩnh viễn ở Sidebar).
  - Nút Logout (`#e74c3c` Đỏ để cảnh báo).

### 3.2. Cột phải (Main Content View)
View nội dung thay đổi theo Sidebar selection.
Chứa các thành phần con với Corner Radius bo tròn, phân cách ranh giới UI bằng các dải màu xám đa tầng (Ví dụ: nền thẻ `gray90` (light) hoặc `gray15` (dark)).

**Chi tiết 4 không gian (Views) chính:**

- **🏠 HomeView (Trang Cấu Hình Chung):** 
  - Nơi đặt Card chứa thông tin định cấu hình: Thư mục lưu file `.md` cục bộ (Nút Browse gọi Context Dialog HĐH).
  - Cấu hình chu kỳ Auto-sync (Dropdown OptionMenu: 15p, 30p, 60p, 3h...) và Switch bật/tắt (Toggle).

- **📝 KeepView (Quản Lý Ghi Chú):** 
  - View lọc và hiển thị nội dung in-memory. Bộ lọc Filter Tag (Dropdown) nằm đầu trang, cùng đếm số bản ghi.
  - Nội dung trình bày dưới dạng thẻ Grid Card (giống Pinterest). Card nào dài quá bị mờ (fade) nội dung ở mép dưới.

- **📓 NLMView (Quản Lý Tích Hợp NotebookLM):** 
  - Đăng nhập phiên NotebookLM qua cửa sổ trình duyệt nhúng hoặc nhập lệnh trực tiếp.
  - Vùng Scrollable chia 2 danh sách phân cực Rõ Ràng (Lưới My Notebooks / Dọc List Sources). 
  - Có Switch để User chủ động bật/tắt tính năng đồng bộ tự động lên AI sau khi sync Keep kết thúc.

- **⏱️ SyncView (Lịch Sử Tương Tác Server):** 
  - Hiển thị thanh tiến trình (Progress Bar) mô phỏng dòng thời gian đang chạy.
  - Vùng Text ScrollableFrame mô phỏng màn dòng lệnh Console Terminal. Có 2 luồng log Console song song: Phía Google Keep (Xử lý file) và Phía NotebookLM (Xử lý tải lên AI).

### 3.3. Extension Browser (Chrome Popup)
Dù là một màn hình phụ trên trình duyệt, UI của Extension (Popup) cần tuân thủ thiết kế mượt mà của Material 3:
- **Giao diện:** Popup kích thước tinh giản (ví dụ: `350x450`). Nền trắng, text xám đậm.
- **Thành phần:** 
  - Nút "🌐 Đăng nhập bằng Google" (màu Xanh `#1A73E8`).
  - Dòng trạng thái (Status Label) cực nhỏ góc dưới (Ví dụ: "✅ Đã uỷ quyền" / "❌ Cần mở tab Google").
  - Nút "🚀 Gửi Token đến Desktop App" (khi đã lấy thành công OAuth).
- **Tương tác:** Nút gửi bị khóa nếu Token chưa sẵn sàng. Sau khi gửi, hiện thông báo Toast Toast ngay trong popup.

---

## 4. TRẢI NGHIỆM NGƯỜI DÙNG CHUNG (GENERAL UX FLOW)

### 4.1. Luồng Onboarding & Đăng nhập (Tích Hợp Extension)
1. Hiển thị Màn hình Đăng nhập (LoginFrame) trên App Desktop.
2. User bấm nút "Mở Trình Duyệt Đăng Nhập" → App kích hoạt mở Extension trên Chrome.
3. Trên Popup Extension: Bấm "Đăng nhập Google", trình duyệt mở trang uỷ quyền `EmbeddedSetup`.
4. Extension tự bắt lấy `oauth_token`, user bấm "Gửi Token đến Desktop".
5. Ứng dụng Desktop phản hồi xoay vòng (Loading state) tiếp nhận Token từ Localhost Server.
6. Desktop nhận xong, hiện Toast đổi màu Xanh êm mượt và Chuyển vào Trang chủ ngay lập tức. Cả App & Extension cùng lưu phiên bảo mật.

### 4.2. Cấu hình ban đầu
- Trải nghiệm 1 click vào nút "Chọn Thư Mục" mở Context Dialog gốc của hệ điều hành.
- Phản hồi trực quan hiển thị ngay đường dẫn mới.

### 4.3. Luồng Đồng bộ (Sync)
1. User nhấn `Sync Now`.
2. Nút bấm bị khoá (Disabled) kèm text "⏳ Đang sync...", tránh việc spam click.
3. Progress bar tại màn "Lịch sử Sync" thể hiện tiến độ (x/y notes).
4. Notification Toast trôi xuống từ đỉnh màn hình với màu Xanh (Thành công) hoặc Đỏ (Lỗi).
5. Nút bấm trở về trạng thái "🔄 Sync Now", StatusBar chân trang cập nhật thời gian Last Sync.

### 4.4. Duyệt Ghi chú (Keep View)
- List render theo Grid 3 cột (Cho trải nghiệm Grid dạng Card tương tự Google Keep gốc).
- Filter Tag & Date tự động fetch Database local hoặc State In-Memory thay vì query trực tiếp lên server Google Keep liên tục để tăng tốc độ phản hồi.
- Nếu Card rỗng → Hiện text Placeholder "Không tìm thấy ghi chú nào".

### 4.5. Luồng Tích Hợp AI (NotebookLM)
1. Truy cập Tab `NotebookLM`. Giao diện empty state hiện "Vui lòng đăng nhập" lớn, kêu gọi hành động (Call To Action).
2. Khi kết nối xong CLI / Account, tải liền danh sách Sổ (Notebooks). Sổ nào được set active sẽ có viền Card nổi bật xanh.
3. Nếu bật Auto-sync to NLM (Switch đang on), mỗi khi ấn lệnh Sync Now gốc (Ở sidebar), App sẽ đính kèm quy trình: Goolge Keep tải về local xong → Load tiếp lên NotebookLM.

---

## 5. CHUYỂN ĐỘNG & TƯƠNG TÁC (MICRO-INTERACTIONS)

- **Toast Notification (Thông báo trôi nhanh):**
  - Vị trí: Ở sát mép trên căn giữa màn hình (`relx=0.5, rely=0.03`).
  - Style: Card nhỏ bo góc, nền Đen mờ `gray20` chữ trắng, hoặc Nền Trắng chữ có Icon tương ứng (Xanh lá / Đỏ / Vàng).
  - Chuyển động: Hiện lên trong vòng 3-4 giây rồi tự xóa bằng hàm `destroy()` hoặc `place_forget()` thông qua `.after(4000)`.
- **Trạng thái Đang Xử Lý (Loading Indicator):**
  - Đặc biệt là các thao tác liên kết mạng (Network Request). Khóa (Disable) ngay nút đã bấm chặn spam.
  - Đổi chữ trên nút sang dạng: "⏳ Đang kết nối..." hoặc "🔄 Đang tải...".
- **Chuyển Tab Menu (Sidebar State):**
  - Menu đang được chọn (Active) sẽ thay đổi màu nền thành Xanh nhạt `#E8F0FE` để User không bao giờ bị lạc đường.

---

## 6. LUỒNG TRẢI NGHIỆM CHI TIẾT (UX FLOW DIAGRAMS)

### 6.1. Luồng Xác thực êm ái qua Chrome Extension (Frictionless Login Flow)
```text
[Mở App] ──> [Đọc config.json lưu trên ổ cứng]
                    │
        [Có sẵn Master Token & Email?]
             ├── CÓ  ──> [Dùng Token thử ping server] 
             │                  └──> Hợp lệ ──> [Bypass Login vào thẳng Trang Chủ]
             │
             └── KHÔNG ──> [Render màn The Login Frame]
                               │
            [User chọn đăng nhập qua Extension]
                               ▼
        [Extension lấy oauth_token -> Ấn Gửi về App Localhost]
                               ▼
    [App khoá giao diện Login -> Hiện Loading lấy Master Token]
                               ▼
            (Bắt ngoại lệ/Error) <── (Thất bại thì hiện báo lỗi Đỏ)
                               ▼ 
      (Lưu Token Mới xuống File config.json + chrome.storage)
                               ▼
             [Trượt/Đổi giao diện vào thẳng Trang Chủ]
```

### 6.2. Luồng Đồng bộ một chạm (One-tap Sync Flow)
```text
[Bấm '🔄 Sync Now']
       │
       ▼
 [Sidebar Button Disabled / Trạng thái đổi thành "⏳ Đang đồng bộ"]
       │
       ▼
 [Kiểm tra Note có thay đổi trong API? (Chỉ sync đồ mới)]
       │ (Tiến trình chạy -> Cập nhật UI Progress Bar nếu đang ở màn Log)
       ▼
 [Xử lý hoàn tất]
       │
       ▼
 [Nảy cái Toast Xanh: "✅ Đã tải thành công X ghi chú"]
       │
       ▼
 [Khôi phục nút 'Sync Now' lại bình thường]
```

### 6.3. Luồng Tìm kiếm & Lọc Tức Thời (Realtime Filter Flow)
```text
[Vào Tab Google Keep] ──> [Tải toàn bộ List File .md Local In-Memory]
                            │
              [Người dùng chọn Tag 'Work']
                            ▼
     [Lọc In-memory danh sách Note không cần load lại từ Internet]
                            ▼
        [Xóa sạch các Card cũ trên màn hình ảo]
                            ▼
              [Render 20 Card phù hợp mới lên]
         (Nếu list mảng=0: Render Text Placeholder "Trống")
```

### 6.4. Luồng Quản Lý Tích Hợp AI (NotebookLM Flow)
```text
[Vào Tab NotebookLM] 
       │
[Đã có Phiên Đăng Nhập chưa?]
       ├── CHƯA ──> [Hiện Hero Card "Vui lòng Đăng Nhập Mới"]
       │                   │
       │                   ▼
       │            [Nhấn nút Đăng Nhập -> Mở form xử lý Auth]
       │                   ▼
       │            [Xong -> Tự động Load Danh sách Notebooks]
       │
       └── RỒI  ──> [Fetch danh sách Notebooks & Nguồn]
                           │
                           ▼
            [Render Grid Notebooks / List Sources]
                           │
                           ▼
    [Nhấn vào 1 Card Notebook bất kỳ -> Viền Card phát sáng (Set Active ID)]
                           │
                           ▼
    [Bật Switch "Đồng bộ NotebookLM" -> App tự động nhớ cấu hình cho lần Sync Keep tới]
```

### 6.5. Luồng Theo Dõi Lịch Sử Đồng Bộ (Sync History Flow)
```text
[Vào Tab Lịch sử Sync]
       │
[Kiểm tra trạng thái app]
       ├── Đang đồng bộ ──> [Thanh Progress Bar chung chạy từ 0% -> 100%]
       │                           │
       │                           ▼
       │                    [Màn hình Terminal chia 2 nửa phân minh]
       │                    │                                      │
       │            (Tiến trình 1 chạy trước)             (Tiến trình 2 chạy sau hoặc song song)
       │                    ▼                                      ▼
       │         [Tải: Keep API ──> Local]             [Đẩy: Local ──> NotebookLM]
       │         - Tạo mới: ...                        - Đọc file ...
       │         - Cập nhật: ...                       - Đăng tải source ...
       │         - Hoàn tất: MÀU XANH                  - Hoàn tất: MÀU XANH
       │                           │
       │                           ▼
       │                    [Màu sắc Log phân định trạng thái rõ: Info (Xám), Success (Xanh), Error (Đỏ)]
       │
       └── Rảnh rỗi   ──> [Hiển thị tiến độ và kết quả 2 bên của lần cuối cùng]
                                   │
                                   ▼
                            [Logs nằm im, có thể cuộn xem lại lỗi nếu có]
```

---
*Phê duyệt bởi: Antigravity Solution Designer - Minh*
