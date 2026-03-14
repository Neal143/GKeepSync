# Phase 01: Setup & Phân tích logic
Status: ⬜ Pending
Dependencies: None

## Objective
Khởi tạo cấu trúc dự án (nếu cần) và phân tích luồng code hiện tại trong file đồng bộ NotebookLM.

## Requirements
### Functional
- [ ] Review lại service lấy danh sách file từ NotebookLM (`api/notebooklm`).
- [ ] Review hàm đồng bộ nội bộ giữa Google Keep và Local.

## Implementation Steps
1. [ ] Đọc file xử lý đồng bộ lên mạng (ví dụ: `syncService` hoặc `notebookLm.ts`).
2. [ ] Xác định vị trí kiểm tra trạng thái file (có ở NotebookLM, có ở Keep, không có ở Local).

## Files to Create/Modify
- Không có thay đổi code trong phase này. Chỉ phân tích và log kết quả.

---
Next Phase: [Phase 02](phase-02-backend.md)
