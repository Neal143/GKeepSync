# Phase 04: NotebookLM Integration
Status: ⬜ Pending | 🟡 In Progress | ✅ Complete
Dependencies: Phase 01

## Objective
Tích hợp giao diện và logic gọi API/CLI của Google NotebookLM để tự động hóa khâu nạp kiến thức cho Notebook.

## Requirements
### Functional
- [ ] Xây dựng `NLMView` với giao diện Đăng Nhập (Hero Card ban đầu).
- [ ] Gọi ngầm lệnh CLI/API để check Auth trạng thái NLM.
- [ ] Lấy danh sách Notebooks (My Notebooks) và Sources tương ứng render lên Layout lưới/danh sách.
- [ ] Chọn và lưu 1 Notebook ID làm Mặc định (Viền sáng màu xanh).
- [ ] Bật/tắt cờ Auto-upload lên sổ tay này.

### Non-Functional
- [ ] Bắt lỗi timeout nếu NotebookLM CLI phản hồi chậm trên Windows.
- [ ] Chuyển đổi trạng thái mượt mà giữa "Chưa đăng nhập" và "Đã tải dữ liệu xong".

## Implementation Steps
1. [ ] Wrap tập lệnh CLI của NotebookLM vào class `NLMService`.
2. [ ] Xây dựng 2 vùng ScrollableFrame cho Notebooks bên trái và Sources bên phải.
3. [ ] Viết chức năng click vào Notebook -> Đổi màu `.configure(border_color="blue")` và lưu ID xuống `config.json`.

## Files to Create/Modify
- `ui/views/nlm_view.py` - Giao diện quản lý sổ tay.
- `core/nlm_service.py` - Wrapper tương tác với server/CLI của NLM.

---
Next Phase: phase-05-sync.md
