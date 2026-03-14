# Plan: Logic đồng bộ xóa file NLM trước khi upload
Created: 2026-03-14T14:30:00+07:00
Status: 🟡 In Progress

## Overview
Xử lý tình huống đặc biệt (edge case) trong quá trình đồng bộ:
**Trường hợp:** File có trên Google Keep và NotebookLM, nhưng **không tồn tại ở kho máy tính (Local)**.
**Hành động:** Khi đồng bộ từ Keep về Local, rồi đẩy từ Local lên NotebookLM, hệ thống bắt buộc phải **XÓA** file đó trên NotebookLM trước, sau đó mới upload file mới lên.
*Mục đích:* Tránh báo lỗi trùng lặp từ NotebookLM và đảm bảo dữ liệu mới nhất được cập nhật sạch sẽ.

## Phases

| Phase | Name | Status | Progress |
|-------|------|--------|----------|
| 01 | Setup & Phân tích logic | ⬜ Pending | 0% |
| 02 | Cập nhật Backend Logic | ⬜ Pending | 0% |
| 03 | Kiểm thử (Testing) | ⬜ Pending | 0% |

## Quick Commands
- Bắt đầu Phase 1: `/code phase-01`
- Kiểm tra tiến độ: `/next`
- Lưu context: `/save-brain`
