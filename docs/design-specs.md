# Design Specifications - GKeepSync (Material 3 - Light Theme)

## 🎨 Color Palette
| Name | Hex | Usage |
|------|-----|-------|
| Primary | #007AFF | Nút bấm chính (Login, Sync), Active State |
| Primary Dark | #0056B3 | Nút bấm chính khi Hover/Pressed |
| Background (App) | #FFFFFF | Nền nội dung chính (Content View) |
| Surface (Sidebar) | #F5F5F7 | Nền Sidebar bên trái |
| Text Primary | #1C1C1E | Tiêu đề, nội dung chính |
| Text Muted | #8E8E93 | Text phụ, ngày tháng, placeholder |
| Danger/Error | #FF3B30 | Thông báo lỗi, nút Xóa/Đăng xuất |
| Success | #34C759 | Icon trạng thái đồng bộ thành công |

## 📝 Typography
*Ưu tiên sử dụng Font hệ thống System Default (San Francisco trên Mac, Segoe UI trên Windows).*

| Element | Font | Size | Weight |
|---------|------|------|--------|
| H1 (App Title) | System | 22px | 700 (Bold) |
| H2 (Section) | System | 18px | 600 (Semibold) |
| Body Text | System | 14px | 400 (Regular) |
| Small / Meta | System | 12px | 400 (Regular) |

## 📐 Spacing System
| Name | Value | Usage |
|------|-------|-------|
| xs | 4px | Khoảng cách giữa Icon và Text |
| sm | 8px | Khoảng cách giữa các item trong list |
| md | 16px | Padding mặc định cho Card/Button |
| lg | 24px | Khoảng cách giữa các Section lớn |

## 🔲 Border Radius
| Name | Value | Usage |
|------|-------|-------|
| sm | 6px | Input fields nhỏ, Checkbox |
| md | 8px | Button vừa, Tag, Menu Item |
| lg | 12px | Card ghi chú, Khối Setting, Input to |

## 🌫️ Shadows
| Name | Value | Usage |
|------|-------|-------|
| sm | Đổ bóng CustomTkinter cực mượt | Dùng cho Note Card khi Hover |

## 🪟 Window & Title Bar
- **Loại Title Bar:** `Native Windows 10/11 Title Bar` (Lựa chọn 1).
- **Lý do:** Đảm bảo độ ổn định cao nhất, hỗ trợ đầy đủ các tính năng bẩm sinh của hệ điều hành như Snap Window, Animation thu nhỏ/phóng to mượt mà của Windows.
- **Kích thước mặc định:** `900x650` (Min: `750x550`).

## 🖼️ MOCKUPS

### 1. Màn hình Login
![Login Mockup](/C:/Users/ADMIN/.gemini/antigravity/brain/f0d8e3c8-da97-4c64-a8b3-6e5e72ff4c27/gkeepsync_login_light_1773169247411.png)

### 2. Màn hình Workspace (Dashboard)
![Dashboard Mockup](/C:/Users/ADMIN/.gemini/antigravity/brain/f0d8e3c8-da97-4c64-a8b3-6e5e72ff4c27/gkeepsync_dashboard_light_1773169264914.png)
