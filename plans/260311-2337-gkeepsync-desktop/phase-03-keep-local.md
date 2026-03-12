# Phase 03: KeepView & Local Data
Status: ⬜ Pending | 🟡 In Progress | ✅ Complete
Dependencies: Phase 02

## Objective
Hoàn thiện Trang Quản Lý Nội Dung Ghi Chú (KeepView) và hệ thống lưu trữ in-memory để truy xuất - lọc file markdown trên ổ cứng cục bộ mượt mà không độ trễ.

## Requirements
### Functional
- [ ] Xây dựng Component tái sử dụng: `NoteCard` (Thẻ Ghi chú 12px bo góc, có bóng).
- [ ] Layout Grid đa cột trong `KeepView`.
- [ ] Xây dựng cỗ máy lọc (Filter Engine) xử lý in-memory theo Tag (Nhãn dán) và Ngày tháng.
- [ ] Logic rỗng (Empty State): Trỏ về Placeholder Text "Không có ghi chú nào".

### Non-Functional
- [ ] Filter theo thời gian thực (Real-time Filtering), chỉ can thiệp bộ nhớ RAM để tăng tốc. Không request lại Google Keep.

## Implementation Steps
1. [ ] Xây dựng `NoteCard` trong `ui/components.py`.
2. [ ] Xây dựng grid manager bằng `.grid()` động trong `KeepView` (Tự rớt dòng).
3. [ ] Viết logic đọc toàn bộ thư mục output `.md`, parse Header metadata để gán Tags hiển thị.

## Files to Create/Modify
- `ui/components.py` - Thêm `NoteCard`.
- `ui/views/keep_view.py` - Grid layout logic.
- `core/local_parser.py` - Đọc quét file hệ thống.

---
Next Phase: phase-04-notebooklm.md
