# tray.py — System tray icon with right-click menu

import threading
import pystray
from PIL import Image, ImageDraw


def _make_amber_dot() -> Image.Image:
    """64×64 amber dot on transparent background."""
    img  = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([6, 6, 58, 58], fill="#e8a020")
    return img


class Tray:
    def __init__(self, settings: dict, callbacks: dict):
        """
        callbacks keys:
            toggle_floating  — callable()
            toggle_taskbar   — callable()
            settings         — callable()
            exit             — callable()
        """
        self._settings  = settings
        self._callbacks = callbacks
        self._icon = pystray.Icon(
            "ClaudeUsageMonitor",
            _make_amber_dot(),
            "Claude Usage Monitor",
            menu=self._build_menu(),
        )

    def _build_menu(self) -> pystray.Menu:
        s = self._settings
        return pystray.Menu(
            pystray.MenuItem(
                "Floating Widget",
                self._toggle_floating,
                checked=lambda item: s.get("show_floating", True),
            ),
            pystray.MenuItem(
                "Taskbar Widget",
                self._toggle_taskbar,
                checked=lambda item: s.get("show_taskbar", True),
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Settings...", self._open_settings),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Exit", self._on_exit),
        )

    # ── Menu handlers ─────────────────────────────────────────────────────────

    def _toggle_floating(self, icon, item):
        if cb := self._callbacks.get("toggle_floating"):
            cb()
        icon.update_menu()

    def _toggle_taskbar(self, icon, item):
        if cb := self._callbacks.get("toggle_taskbar"):
            cb()
        icon.update_menu()

    def _open_settings(self, icon, item):
        if cb := self._callbacks.get("settings"):
            cb()

    def _on_exit(self, icon, item):
        icon.stop()
        if cb := self._callbacks.get("exit"):
            cb()

    # ── Lifecycle ─────────────────────────────────────────────────────────────

    def start(self):
        threading.Thread(target=self._icon.run, daemon=True).start()

    def stop(self):
        try:
            self._icon.stop()
        except Exception:
            pass
