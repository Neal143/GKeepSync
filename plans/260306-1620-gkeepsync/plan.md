# Plan: GKeepSync Desktop App
Created: 2026-03-06 16:20
Status: 🟡 In Progress

## Overview
App Windows đồng bộ Google Keep → thư mục local. Giao diện CustomTkinter, auth bằng Master Token, lọc theo tag/thời gian, auto + manual sync. Build thành .exe bằng PyInstaller.

## Tech Stack
- **Language:** Python 3.11+
- **GUI:** CustomTkinter 5.x
- **Google Keep:** gkeepapi + gpsoauth
- **Build:** PyInstaller
- **Config:** JSON file (lưu token, settings)

## Architecture

```
GKeepSync/
├── main.py                    # Entry point
├── app.py                     # Main application window
├── config.py                  # Config management (token, settings)
├── keep_client.py             # gkeepapi wrapper
├── sync_engine.py             # Sync logic + scheduler
├── ui/
│   ├── __init__.py
│   ├── login_frame.py         # Login UI (nhập Master Token)
│   ├── main_frame.py          # Main UI (danh sách notes, controls)
│   ├── settings_frame.py      # Settings UI (thư mục, auto sync interval)
│   └── components.py          # Reusable UI components
├── utils/
│   ├── __init__.py
│   ├── markdown_converter.py  # Convert Keep note → .md
│   └── logger.py              # Logging utility
├── assets/
│   └── icon.ico               # App icon
├── requirements.txt
├── build.spec                 # PyInstaller spec file
└── README.md
```

## Phases

| Phase | Name | Status | Progress |
|-------|------|--------|----------|
| 01 | Setup & Dependencies | ⬜ Pending | 0% |
| 02 | Core Engine (Keep Client + Sync) | ⬜ Pending | 0% |
| 03 | GUI (CustomTkinter) | ⬜ Pending | 0% |
| 04 | Integration & Polish | ⬜ Pending | 0% |
| 05 | Build .exe (PyInstaller) | ⬜ Pending | 0% |

## Quick Commands
- Start Phase 1: `/code phase-01`
- Check progress: `/next`
