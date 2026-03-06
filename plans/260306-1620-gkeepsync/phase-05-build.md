# Phase 05: Build .exe (PyInstaller)
Status: ⬜ Pending
Dependencies: Phase 04

## Objective
Đóng gói app thành file .exe duy nhất chạy được trên Windows.

## Implementation Steps
1. [ ] Tạo `build.spec` cho PyInstaller:
   - `--onefile` → 1 file .exe duy nhất
   - `--noconsole` → không hiện terminal
   - `--add-data` → include CustomTkinter assets
   - `--icon` → app icon
2. [ ] Xử lý CustomTkinter path trong PyInstaller
3. [ ] Build và test .exe
4. [ ] Tạo `README.md` hướng dẫn:
   - Cách lấy Master Token
   - Cách sử dụng app
   - Troubleshooting

## Build Command
```
pyinstaller --noconfirm --onefile --noconsole \
  --add-data "customtkinter_path;customtkinter/" \
  --icon=assets/icon.ico \
  --name=GKeepSync \
  main.py
```

## Files to Create
- `build.spec`
- `README.md`

## Test Criteria
- [ ] Build thành công, tạo được file .exe
- [ ] .exe chạy được trên máy KHÔNG cài Python
- [ ] UI hiển thị đúng (fonts, theme)
- [ ] Login + Sync hoạt động bình thường từ .exe
