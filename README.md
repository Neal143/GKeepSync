# 🔄 GKeepSync

Đồng bộ Google Keep → thư mục local dưới dạng file Markdown (.md).

## ✨ Tính năng

- 📥 **Sync ghi chú** từ Google Keep về thư mục local
- 🏷️ **Lọc theo tag** — chỉ sync những ghi chú có label mong muốn
- 📅 **Lọc theo thời gian** — chọn khoảng ngày cần sync
- ⏰ **Auto Sync** — tự động đồng bộ theo thời gian cài đặt (15p / 30p / 1h / 3h / 6h)
- 👆 **Manual Sync** — bấm nút Sync Now bất cứ lúc nào
- 📝 **Xem danh sách** ghi chú đã sync ngay trong app
- 🌙 **Dark mode** đẹp mắt

## 🚀 Cài đặt

### Cách 1: Chạy file .exe (Không cần Python)
1. Tải file `GKeepSync.exe` từ thư mục `dist/`
2. Chạy trực tiếp

### Cách 2: Chạy từ source
```bash
# Clone repo
cd "Gkeepsync app"

# Tạo virtual environment
python -m venv venv
venv\Scripts\activate

# Cài dependencies
pip install -r requirements.txt

# Chạy app
python main.py
```

## 🔑 Cách lấy Master Token

> **Lưu ý:** `gkeepapi` là thư viện không chính thức. Bạn cần Master Token để xác thực.

### Bước 1: Bật 2FA
- Vào [myaccount.google.com](https://myaccount.google.com)
- Bật xác minh 2 bước (2-Step Verification)

### Bước 2: Tạo App Password
- Vào tab **Security** (Bảo mật).
- Tìm mục **"How you sign in to Google"** (Cách bạn đăng nhập vào Google).
- Click vào dòng **2-Step Verification** (Xác minh 2 bước) — click đúng vào dấu mũi tên ở cuối dòng.
- Cuộn xuống dưới cùng của trang đó, bạn sẽ thấy mục **App passwords** (Mật khẩu ứng dụng).
- Tạo mật khẩu mới cho ứng dụng "Other" (Đặt tên tùy ý, ví dụ: GKeepSync).

### Bước 3: Đăng nhập vào GKeepSync
- Mở app GKeepSync
- Nhập **Email** của bạn
- Nhập **App Password** (16 ký tự) vừa tạo vào ô Password
- Bấm **Kết nối** (App sẽ tự động lấy Master Token và lưu lại cho các lần sau)

## 📁 Format file .md

Mỗi ghi chú được lưu dạng Markdown với YAML frontmatter:

```markdown
---
title: "Tên ghi chú"
tags: ["tag1", "tag2"]
created: 2024-01-15 10:30:00
updated: 2024-01-15 14:20:00
keep_id: "abc123"
---

# Tên ghi chú

Nội dung ghi chú ở đây...
```

## 🔨 Build .exe

```bash
# Activate venv
venv\Scripts\activate

# Build
pyinstaller build.spec

# File .exe sẽ ở: dist/GKeepSync.exe
```

## ⚠️ Lưu ý

- `gkeepapi` là thư viện **không chính thức**, Google có thể chặn bất cứ lúc nào
- Master Token nên được giữ bí mật (app lưu trong `%APPDATA%/GKeepSync/config.json`)
- Sync **1 chiều** (Keep → Local), không sửa/xóa ghi chú trên Keep
