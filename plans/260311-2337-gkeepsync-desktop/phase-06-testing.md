# Phase 06: Testing & Refinement
Status: ⬜ Pending | 🟡 In Progress | ✅ Complete
Dependencies: All previous phases

## Objective
Rà soát lại toàn bộ chuẩn Material 3, gỡ lỗi Edge-cases (mạng mẽo, token hết hạn) và đóng gói bản phát hành EXE.

## Requirements
### Functional
- [ ] Edge Case: App Password/Master Token bị Google từ chối -> Báo văng ra màn đăng nhập.
- [ ] Edge Case: Mạng mất giữa chừng lúc đang tải Note -> Báo lỗi đỏ không crash.
- [ ] Đóng gói toàn bộ Image/Font/Theme vào chung file `.exe` qua PyInstaller.

### Non-Functional
- [ ] UI Audit: Kiểm tra lại các chỗ giật, lag. Mọi nút bấm đều phải có hiệu ứng Hover màu Xanh nhạt.
- [ ] RAM Optimization: Check xem Threading có bị rò rỉ bộ nhớ (Memory leak) sau 12 tiếng treo ngầm hay không.

## Implementation Steps
1. [ ] Chạy manual test 4 kịch bản Auth (Ext có Email, Ext không Email, Thủ công, Lỗi mạng).
2. [ ] Kiểm tra Hover states từng góc ngách.
3. [ ] Chèn `.spec` rà soát Build file.

## Files to Create/Modify
- `gkeepsync.spec` - Cấu hình build.
- *(Misc fixes across codebase)*

---
Next Phase: GO LIVE 🚀
