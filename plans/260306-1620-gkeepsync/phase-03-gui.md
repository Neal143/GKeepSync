# Phase 03: GUI (CustomTkinter)
Status: ⬜ Pending
Dependencies: Phase 02

## Objective
Xây dựng giao diện đồ họa hoàn chỉnh với CustomTkinter. Dark theme, hiện đại.

## UI Layout

```
┌─────────────────────────────────────────────────────────┐
│  🔄 GKeepSync                              [─] [□] [×] │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─── LOGIN FRAME (hiện lúc đầu) ────────────────────┐ │
│  │  📧 Email: [________________]                      │ │
│  │  🔑 Master Token: [________________]              │ │
│  │        [  Connect  ]                              │ │
│  │  ℹ️ Hướng dẫn lấy Master Token                    │ │
│  └────────────────────────────────────────────────────┘ │
│                                                         │
│  ┌─── MAIN FRAME (sau khi login) ────────────────────┐ │
│  │  📁 Output: D:\Notes\Keep  [Browse]               │ │
│  │                                                    │ │
│  │  ── FILTERS ──────────────────────────────────     │ │
│  │  🏷️ Tags:  [All ▼]                                │ │
│  │  📅 From:  [____-__-__]  To: [____-__-__]        │ │
│  │                                                    │ │
│  │  ── AUTO SYNC ────────────────────────────────     │ │
│  │  ⏰ Interval: [15 min ▼]  [ ] Enabled             │ │
│  │                                                    │ │
│  │  [  🔄 Sync Now  ]                                │ │
│  │                                                    │ │
│  │  ── NOTES LIST ───────────────────────────────     │ │
│  │  │ 📝 Note Title 1        │ 2024-01-15 │ tag1 │   │ │
│  │  │ 📝 Note Title 2        │ 2024-01-14 │ tag2 │   │ │
│  │  │ 📝 Note Title 3        │ 2024-01-13 │      │   │ │
│  │  │ ...                                        │   │ │
│  │                                                    │ │
│  │  ── STATUS BAR ───────────────────────────────     │ │
│  │  ✅ Last sync: 15:30 | 42 notes | Next: 15:45    │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## Implementation Steps
1. [ ] `app.py` — Main window (CTk), quản lý frame switching
2. [ ] `ui/login_frame.py` — Form nhập email + token, nút Connect
3. [ ] `ui/main_frame.py` — Giao diện chính:
   - Folder picker
   - Tag filter dropdown (load từ Keep labels)
   - Date range pickers
   - Auto sync toggle + interval selector
   - Sync Now button
   - Notes table/list (scrollable)
   - Status bar (last sync, count, next sync time)
4. [ ] `ui/settings_frame.py` — Settings nếu cần tách riêng
5. [ ] `ui/components.py` — Reusable widgets (date picker, status bar)
6. [ ] Dark theme + modern styling

## Files to Create
- `app.py`
- `ui/login_frame.py`
- `ui/main_frame.py`
- `ui/settings_frame.py`
- `ui/components.py`

## Test Criteria
- [ ] App mở lên hiển thị Login frame
- [ ] Sau khi login → chuyển sang Main frame
- [ ] Tất cả controls hoạt động (dropdown, date picker, buttons)
- [ ] Notes list hiển thị đúng dữ liệu
- [ ] Status bar cập nhật real-time
