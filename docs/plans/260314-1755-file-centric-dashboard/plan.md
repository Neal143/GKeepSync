# Plan: File-Centric Sync Dashboard
Created: 2026-03-14 17:55
Status: 🟡 In Progress

## Overview
Đập bỏ hoàn toàn giao diện Terminal text-based cũ, thay bằng một **Bảng danh sách file (DataGrid)** trực quan. Bảng này sẽ tổng hợp chéo trạng thái của một note (từ Keep -> Local và Local -> NLM) trên cùng một dòng, cho phép người dùng nhìn tổng quan và bám sát vòng đời của file. Tính năng này bao hàm việc tạo một RAM State Tracker (Bộ lưu trạng thái tạm thời) ở backend.

## Tech Stack
- UI: customtkinter (Grid Layout / ScrollableFrame)
- Logic State: Python Dictionary (Ram-based)
- Integrations: sync_engine.py, nlm_worker.py

## Phases

| Phase | Name | Status | Progress |
|-------|------|--------|----------|
| 01 | State Tracking Mechanism | ⬜ Pending | 0% |
| 02 | Frontend UI Grid | ⬜ Pending | 0% |
| 03 | Testing & Refinement | ⬜ Pending | 0% |

## Quick Commands
- Start Phase 1: `/code phase-01`
- Check progress: `/next`
- Save context: `/save-brain`
