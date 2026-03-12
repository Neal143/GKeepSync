# Phase 05: Sync Engine & SyncView
Status: ⬜ Pending | 🟡 In Progress | ✅ Complete
Dependencies: Phase 02, Phase 04

## Objective
Trái tim của ứng dụng: Xây dựng động cơ Đồng bộ tự động 2 chiều (Keep -> Local -> NLM) và hiển thị log real-time đẹp mắt.

## Requirements
### Functional
- [ ] Loop chạy nền (Background thread) kiểm tra chu kỳ Auto-sync.
- [ ] Hàm so sánh Last Modified: Chỉ tải file thực sự thay đổi từ Google Keep.
- [ ] Nếu NLM_Auto_Upload = True: Gọi tiếp hàm đẩy từ Local -> NotebookLM.
- [ ] UI `SyncView` chia 2 cột Log (Keep Log, NLM Log). Cập nhật màu text (Red/Green/Gray) real-time.

### Non-Functional
- [ ] Sync chạy ở Thread riêng rẽ (`threading.Thread`) để không làm đơ (freeze) giao diện App.
- [ ] Bắt cực chặt Exception mất mạng (ConnectionError) để không sập app, chỉ văng Log đỏ.

## Implementation Steps
1. [ ] Khởi tạo Threading Manager cho quá trình Sync.
2. [ ] Xây dựng Layout Terminal giả lập với Progress Bar tổng.
3. [ ] Viết logic parse màu cho Text widget của Tkinter (`tag_config`).

## Files to Create/Modify
- `core/sync_engine.py` - Logic chạy ngầm Threading.
- `ui/views/sync_view.py` - Giao diện Console.
- `main.py` - Khởi động Scheduler ngay lúc bật App.

---
Next Phase: phase-06-testing.md
