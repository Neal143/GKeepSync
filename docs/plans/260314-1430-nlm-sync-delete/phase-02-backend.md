# Phase 02: Cập nhật Backend Logic
Status: ⬜ Pending
Dependencies: phase-01-setup.md

## Objective
Chỉnh sửa logic đồng bộ cốt lõi để bao gồm điều kiện xóa trước khi upload.

## Requirements
### Functional
- [ ] Thêm điều kiện: `if (!existsInLocal && existsInNotebookLM && existsInKeep)`
- [ ] Thực hiện gọi API/CLI xóa file trên NotebookLM ứng với file đó.
- [ ] Sau khi xóa thành công, tiếp tục quy trình chuẩn (tùy chọn: download từ Keep -> lưu Local -> upload lên NotebookLM mới).

## Implementation Steps
1. [ ] Step 1: Chèn logic kiểm tra.
2. [ ] Step 2: Gắn hàm gọi `notebooklm mcp delete <target_id>` (hoặc tương đương) trước khi tiến hành upload.
3. [ ] Step 3: Đảm bảo xử lý lỗi (fallback) nếu việc xóa thất bại.

## Files to Create/Modify
- Các file service liên quan đồng bộ.

---
Next Phase: [Phase 03](phase-03-testing.md)
