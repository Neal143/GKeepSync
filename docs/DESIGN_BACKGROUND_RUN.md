# 🎨 DESIGN: Tính năng Khởi động cùng Windows & Chạy ngầm & Lưu Cấu hình

Ngày tạo: 13/03/2026
Dựa trên: `docs/BRIEF_BACKGROUND_RUN.md`

---

## 1. Mở rộng Cấu trúc Lưu trữ (Config JSON)

Hiện tại, app dùng file `config.json` thông qua `config.py`. Mình sẽ **không tạo thêm file mới** mà sẽ mở rộng file này.

**Sự thay đổi trong `DEFAULT_CONFIG`:**
```python
DEFAULT_CONFIG = {
    # Cũ:
    "output_folder": "...",      # Đường dẫn thư mục local lưu Markdown
    "nlm_notebook_id": "",       # ID cuốn sổ trên Google Keep
    
    # MỚI THÊM:
    "run_on_startup": False      # Tùy chọn: Có khởi động cùng máy tính không? (Mặc định: Tắt)
}
```

*Giải thích:*
- **Lưu cấu hình Local Folder và Notebook:** 2 dữ liệu này thực chất đã có sẵn biến lưu trữ (`output_folder` và `nlm_notebook_id`), phần thiết kế sẽ tập trung vào việc **gọi hàm load và móc nối (bind)** dữ liệu này vào Cửa sổ Giao diện (Tkinter) khi app vừa phóng lên.
- **Biến `run_on_startup`:** Sẽ nối với 1 Checkbox mới ở giao diện.

---

## 2. Danh Sách Màn Hình / Giao Diện Cần Thêm

| Tên | Vị trí | Thao tác người dùng |
|-----|--------|---------------------|
| **Checkbox "Khởi động cùng Windows"** | Màn hình Chính (Khu vực Cấu hình Đồng bộ) | Tick/Bỏ tick để bật/tắt tính năng khởi động cùng máy. |
| **System Tray Icon (Icon góc phải máy tính)** | Taskbar máy tính | Hiển thị khi app đang mở hoặc đang chạy ngầm. |
| **Context Menu của Icon** | Chuột phải vào Icon ở góc phải | Hiện menu với 3 nút: **Mở App**, **Đồng bộ ngay**, **Thoát hẳn App**. |

---

## 3. Luồng Hoạt Động (User Journey)

### 📍 HÀNH TRÌNH 1: Khởi động & Điền tự động
1. User mở app.
2. Background: App đọc `config.json`.
3. Giao diện hiện lên.
4. Tự động điền đường dẫn thư mục vào ô "Local Folder".
5. Tự động chọn đúng Notebook trong dropdown "Notebook".
6. User không cần bấm chọn lại, có thể bấm "Sync" luôn.

### 📍 HÀNH TRÌNH 2: Tắt chạy ngầm thay vì thoát luôn
1. User bấm **[X] đỏ** ở góc trên cửa sổ.
2. Background: App chặn lệnh tắt hẳn (Destroy Window).
3. App ẩn giao diện đi (withdraw), nhưng icon dưới góc phải (System Tray) vẫn hiện.
4. Ứng dụng vẫn âm thầm chạy Auto-sync theo chu kỳ đã hẹn (nếu có hẹn).

### 📍 HÀNH TRÌNH 3: Bật tự động khởi động cùng Windows
1. User tick vào ô "Khởi động cùng Windows".
2. Background: App gọi API của Windows (tạo lối tắt trong Startup folder hoặc Registry key).
3. Hôm sau, khi bật máy tính lên, app tự động mở to lên nhờ cái Shortcut Windows vừa gọi.

---

---

## 4. Test Cases (Checklist Kiểm Tra) — ✅ ĐÃ HOÀN THÀNH

### 🧪 TC-01: Auto-Fill cấu hình khi bật app — ✅
- **Given:** Ở lần dùng trước, User chọn folder `D:/MyNotes` và sổ Notebook là `Nhật ký`. Đã thoát app.
- **When:** User mở lại app (Start GKeepSync).
- **Then:** 
  ✓ Ô Folder Path hiện sẵn `D:/MyNotes`.
  ✓ Dropdown Notebook tự chọn sẵn `Nhật ký`.

### 🧪 TC-02: Chạy ngầm thay vì Tắt — ✅
- **Given:** App đang hiện trên màn hình.
- **When:** Bấm [X] đỏ để đóng cửa sổ.
- **Then:** 
  ✓ Cửa sổ biến mất khỏi màn hình và thanh Taskbar chính.
  ✓ Icon nhỏ của app hiện dưới System Tray (góc phải màn hình).
  ✓ Task Manager vẫn thấy process python/GKeepSync đang chạy.

### 🧪 TC-03: Menu System Tray (Mở / Thoát) — ✅
- **Given:** App đang chạy ngầm (chỉ có icon dưới System Tray).
- **When:** Chuột phải vào Icon, chọn "Mở App".
- **Then:**
  ✓ Cửa sổ App pop-up lên giữa màn hình.
- **When:** Chuột phải vào Icon, chọn "Thoát hẳn App".
- **Then:**
  ✓ Icon biến mất.
  ✓ Process bị kill hoàn toàn trong Task Manager.

### 🧪 TC-04: Khởi động cùng Windows — ✅
- **Given:** App đang mở, User tick vào Checkbox "Khởi động cùng Windows".
- **When:** Khởi động lại máy tính (Restart PC).
- **Then:** 
  ✓ Ngay khi Windows lên, GKeepSync tự chạy ngầm vào System Tray (không hiện cửa sổ, KHÔNG có Ghost Window).
  ✓ Chạy kiểm tra TC-01 thấy dữ liệu vẫn auto-fill đúng.

> **Ghi chú kỹ thuật:** Ghost Window được xử lý bằng `alpha=0.0` trước khi gọi `withdraw()`. Khởi động qua Startup Folder với flag `--start-hidden`.

---
*Tạo bởi AWF 4.0 - Design Phase | Cập nhật: 2026-03-14*
