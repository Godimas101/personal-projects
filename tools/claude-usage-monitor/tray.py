# tray.py — System tray icon with right-click menu

import threading
import pystray
from PIL import Image, ImageDraw
import theme as T


def _make_icon(session_pct: float = 0.0) -> Image.Image:
    """64×64 pie chart showing session usage %."""
    size = 64
    pad  = 3
    img  = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Dark background circle
    draw.ellipse([pad, pad, size - pad, size - pad], fill="#0f0e0c")

    # Filled pie slice — starts at 12 o'clock, sweeps clockwise
    pct   = max(0.0, min(1.0, session_pct / 100))
    color = T.usage_colour(pct)
    inner = pad + 5
    if pct >= 1.0:
        draw.ellipse([inner, inner, size - inner, size - inner], fill=color)
    elif pct > 0.0:
        end_angle = -90 + pct * 360
        draw.pieslice([inner, inner, size - inner, size - inner],
                      start=-90, end=end_angle, fill=color)

    # Dim ring showing the full circle boundary
    draw.ellipse([inner, inner, size - inner, size - inner],
                 outline=T.AMBER_DIM, width=1)

    # Outer border
    draw.ellipse([pad, pad, size - pad, size - pad],
                 outline=T.BORDER, width=1)

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
