# Phase 02: Frontend UI Grid
Status: ⬜ Pending
Dependencies: [Phase 01](phase-01-state-tracking.md)

## Objective
Xây dựng lớp Giao diện (Frontend View) hiển thị bảng State từ RAM ra màn hình. Thay thế hoàn toàn Terminal Log Cũ bằng UI DataGrid mới có Scroll.

## Requirements
### Functional
- [ ] Render 1 khu vực Banner Summary: TỔNG (x), THÀNH CÔNG (y), BỎ QUA (z), LỖI (w).
- [ ] Render 1 khu vực DataGrid với các cột chính: TÊN FILE, TẢI TỪ GOOGLE KEEP, ĐẨY LÊN NLM.
- [ ] Cập nhật Real-time (tức thì): Mỗi khi State RAM dict ở Backend đổi trạng thái (VD: Từ `⏳ Đang tải` sang `✅ Xong`), lập tức dòng File ở trên Giao diện phải đổi biểu tượng Text tương ứng mà không cần Render lại toàn bộ bảng.

### Non-Functional
- [ ] Auto-scroll khi dánh sách dài.
- [ ] Layout cân đối, căn trái cho Tên File và căn giữa/thẳng hàng cho các Cột Status để dễ gióng mắt.
- [ ] Hover effect để làm nổi bật dòng đang xem (Optional, Customizable using frame bg color update).

## Implementation Steps
1. [ ] Xóa/Ẩn widget Terminal cũ (`keep_log_scroll`, `nlm_log_scroll`, `shared_log_scroll`).
2. [ ] Thêm frame Banner Summary (4 Labels ngang hiển thị con số).
3. [ ] Xây dựng 1 Header mô phỏng tiêu đề các cột: `| File Name | Google Keep | NotebookLM |`
4. [ ] Tạo vòng lặp Row-Frame động mỗi khi State Dict nhận 1 File Name mới. Thiết kế mỗi Row là 1 thẻ. 
5. [ ] Tạo hàm Update UI để lắng nghe tín hiệu của Backend (từ Phase 1) và đổi label symbol `✅, ❌, ⚪, ⏳`.

## Files to Modify
- `ui/views/sync_view.py`
- `ui/themes/colors.py` (nếu cần thêm màu cho các icon mới).

---
Next Action: Final testing and code review.
