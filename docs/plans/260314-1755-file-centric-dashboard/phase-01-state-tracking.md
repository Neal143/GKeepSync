# Phase 01: State Tracking Mechanism
Status: ⬜ Pending
Dependencies: None

## Objective
Xây dựng một Class nhỏ gọn hoặc Memory State (Dictionary) nằm bên dưới giao diện `SyncView` / `SyncEngine` để duy trì dòng đời của một File trong suốt tiến trình Sync, làm nguồn cấp dữ liệu (data source) cho Bảng Giao Diện mới.

## Requirements
### Functional
- [ ] Cho phép đăng ký một File mới vào State.
- [ ] Có thể Tracking 2 đầu công việc độc lập: `Keep Process` và `NLM Process` trên cùng 1 File.
- [ ] Hỗ trợ đầy đủ các StateEnum: `PENDING (⏳)`, `SUCCESS (✅)`, `SKIPPED (⚪)`, `ERROR (❌)`.

### Non-Functional
- [ ] State chỉ lưu trên RAM (Dict), dọn dẹp mỗi lần phiên Sync diễn ra. Không đè nén vào database SQLite để tránh chậm máy và out of sync.

## Implementation Steps
1. [ ] Cấu hình các State Status Constant Enum (`STATUS_PENDING`, `STATUS_SUCCESS`...)
2. [ ] Sửa lại logic Callback từ Backend `sync_engine.py` để phát tín hiệu (signal) chứa TÊN FILE + BƯỚC (Keep hay NLM) + KẾT QUẢ.
3. [ ] View hoặc Engine tiếp nhận tín hiệu để set/update State_Dict.

## Files to Modify
- `sync_engine.py` - Cập nhật callback.
- `ui/views/sync_view.py` - Đón tín hiệu update state.

---
Next Phase: [Phase 02](phase-02-ui-grid.md)
