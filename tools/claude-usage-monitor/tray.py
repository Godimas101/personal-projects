# tray.py — System tray icon with right-click menu

import threading
import pystray
from PIL import Image, ImageDraw


def _make_icon(session_pct: float = 0.0) -> Image.Image:
    """64×64 amber dot with session % text."""
    img  = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([4, 4, 60, 60], fill="#e8a020")

    text = f"{int(session_pct)}%"
    try:
        from PIL import ImageFont
        font = ImageFont.truetype("arialbd.ttf", 22)
    except Exception:
        try:
            from PIL import ImageFont
            font = ImageFont.truetype("arial.ttf", 22)
        except Exception:
            font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text(((64 - tw) // 2, (64 - th) // 2 - 1), text, fill="#1a0e00", font=font)
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
            _make_icon(0.0),
            "Claude Usage Monitor",
            menu=self._build_menu(),
        )

    def update_usage(self, rate_data, local_stats) -> None:
        """Update tray icon with current session %."""
        try:
            pct = rate_data.five_hour_pct if rate_data else 0.0
            self._icon.icon = _make_icon(pct)
            self._icon.title = f"Claude Usage Monitor — Session {int(pct)}%"
        except Exception:
            pass

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
        # Delay so tkinter thread updates settings before menu re-reads them
        threading.Timer(0.4, icon.update_menu).start()

    def _toggle_taskbar(self, icon, item):
        if cb := self._callbacks.get("toggle_taskbar"):
            cb()
        threading.Timer(0.4, icon.update_menu).start()

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
