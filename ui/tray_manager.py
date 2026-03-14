"""
GKeepSync - Tray Manager
Xử lý các tác vụ liên quan đến Icon Khay hệ thống (System Tray).
(Tách ra từ app.py để giảm tải God Object)
"""

import threading
import pystray
from PIL import Image, ImageDraw


class TrayManager:
    """Quản lý icon Pystray dưới khay hệ thống, không chặn mainloop của Tkinter."""

    def __init__(self, app_instance):
        self.app = app_instance
        self.icon = None

    def _create_default_icon(self) -> Image.Image:
        """Create a simple icon if no assets/icon.png exists."""
        image = Image.new('RGB', (64, 64), color=(52, 152, 219))
        dc = ImageDraw.Draw(image)
        dc.rectangle([16, 16, 48, 48], fill=(255, 255, 255))
        return image

    def _get_nlm_status_text(self, item):
        """Returns the dynamic text for NLM status in the tray."""
        is_signed_in = getattr(self.app, 'nlm_signed_in', False)
        # Sử dụng Emoji để thể hiện màu sắc trên Windows Tray Menu (vì text thuần không hỗ trợ đổi màu)
        return "✅ NotebookLM: Đã đăng nhập" if is_signed_in else "❌ NotebookLM: Chưa đăng nhập"

    def _do_nothing(self, icon, item):
        pass

    def _is_nlm_disconnected(self, item):
        """Returns True if NLM is NOT signed in, making the item bold (default)."""
        return not getattr(self.app, 'nlm_signed_in', False)

    def hide_to_tray(self):
        """Mục tiêu [MVP-3]: Thu nhỏ xuống khay hệ thống thay vì đóng."""
        self.app.withdraw()  # Ẩn cửa sổ Tkinter chính
        
        # Chỉ tạo icon nếu chưa có
        if self.icon is None:
            try:
                icon_image = Image.open("assets/icon.png")
            except Exception:
                icon_image = self._create_default_icon()

            menu = pystray.Menu(
                # Use default=self._is_nlm_disconnected to make it bold conditionally
                pystray.MenuItem(self._get_nlm_status_text, self._do_nothing, enabled=False, default=self._is_nlm_disconnected),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("Mở App", self._on_show_clicked, default=False),
                pystray.MenuItem("Đồng bộ ngay", self._on_sync_clicked),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("Thoát hẳn App", self._on_quit_clicked)
            )

            self.icon = pystray.Icon("GKeepSync", icon_image, "GKeepSync", menu)
        
        # Chạy icon trên thread riêng để không block Main thread Tkinter
        threading.Thread(target=self.icon.run, daemon=True).start()

    def _on_show_clicked(self, icon=None, item=None):
        """Khôi phục cửa sổ từ System Tray."""
        if self.icon:
            self.icon.stop()
            self.icon = None
        
        # Forward logic hiển thị (với fix tàng hình tk) về lại hàm của app
        self.app.after(0, self.app.restore_from_tray)

    def _on_sync_clicked(self, icon=None, item=None):
        """Handle sync từ System Tray an toàn (forward về Main Thread)."""
        if self.app._config.has_credentials:
            self.app.after(0, self.app.force_sync_from_tray)

    def _on_quit_clicked(self, icon=None, item=None):
        """Thoát hoàn toàn ứng dụng từ System Tray."""
        if self.icon:
            self.icon.stop()
        self.app.after(0, self.app.quit_app_entirely)

    def stop(self):
        """Dừng icon (Dùng khi MainApp đóng hẳn)."""
        if self.icon:
            self.icon.stop()
            self.icon = None
