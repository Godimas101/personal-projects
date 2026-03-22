# win_utils.py — Win32 helpers: screen lock detection, taskbar positioning

import ctypes
from ctypes import wintypes


# ── Screen lock / screensaver detection ───────────────────────────────────────

def is_screensaver_active() -> bool:
    """Returns True if a screensaver is currently running."""
    active = ctypes.c_bool()
    # SPI_GETSCREENSAVERRUNNING = 0x0072
    ctypes.windll.user32.SystemParametersInfoA(0x0072, 0, ctypes.byref(active), 0)
    return active.value


def is_workstation_locked() -> bool:
    """Returns True if the workstation is locked (Ctrl+L / Win+L)."""
    # OpenInputDesktop returns NULL when the desktop is inaccessible
    # DESKTOP_SWITCHDESKTOP = 0x0100
    hDesk = ctypes.windll.user32.OpenInputDesktop(0, False, 0x0100)
    if hDesk:
        ctypes.windll.user32.CloseDesktop(hDesk)
        return False
    return True


def is_fullscreen() -> bool:
    """Returns True if a fullscreen or borderless-fullscreen app is in the foreground."""
    try:
        # SHQueryUserNotificationState: 3=D3D fullscreen, 4=presentation mode
        state = ctypes.c_int(0)
        ctypes.windll.shell32.SHQueryUserNotificationState(ctypes.byref(state))
        if state.value in (3, 4):
            return True
        # Also catch borderless fullscreen (covers entire screen rect)
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        if hwnd:
            # Exclude the Windows desktop itself (clicking desktop = Progman/WorkerW foreground)
            cls_buf = ctypes.create_unicode_buffer(256)
            ctypes.windll.user32.GetClassNameW(hwnd, cls_buf, 256)
            if cls_buf.value in ("Progman", "WorkerW"):
                return False
            rect = wintypes.RECT()
            ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
            sw = ctypes.windll.user32.GetSystemMetrics(0)  # SM_CXSCREEN
            sh = ctypes.windll.user32.GetSystemMetrics(1)  # SM_CYSCREEN
            if rect.left <= 0 and rect.top <= 0 and rect.right >= sw and rect.bottom >= sh:
                return True
    except Exception:
        pass
    return False


def should_pause() -> bool:
    """Returns True if the widget should pause all polling.

    Covers both workstation lock (Win+L) and active screensaver.
    This is THE fix for the bug that plagued the previous widget.
    """
    return is_screensaver_active() or is_workstation_locked()


# ── Taskbar / tray positioning ────────────────────────────────────────────────

def get_tray_rect() -> wintypes.RECT:
    """Return the bounding RECT of the system tray notification area."""
    taskbar = ctypes.windll.user32.FindWindowA(b"Shell_TrayWnd", None)
    tray    = ctypes.windll.user32.FindWindowExA(taskbar, None, b"TrayNotifyWnd", None)
    rect    = wintypes.RECT()
    ctypes.windll.user32.GetWindowRect(tray, ctypes.byref(rect))
    return rect


def get_taskbar_rect() -> wintypes.RECT:
    """Return the bounding RECT of the full taskbar."""
    taskbar = ctypes.windll.user32.FindWindowA(b"Shell_TrayWnd", None)
    rect    = wintypes.RECT()
    ctypes.windll.user32.GetWindowRect(taskbar, ctypes.byref(rect))
    return rect


# ── Window style helpers ──────────────────────────────────────────────────────

GWL_STYLE        = -16
GWL_EXSTYLE      = -20
WS_POPUP         = 0x80000000
WS_CHILD         = 0x40000000
WS_CLIPSIBLINGS  = 0x04000000
WS_VISIBLE       = 0x10000000
WS_EX_TOOLWINDOW = 0x00000080
WS_EX_APPWINDOW  = 0x00040000
WS_EX_NOACTIVATE = 0x08000000
SWP_FRAMECHANGED = 0x0020
SWP_SHOWWINDOW   = 0x0040


def set_tool_window(hwnd: int) -> None:
    """Make a window a tool window: removes taskbar button, hides from Alt+Tab."""
    style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    style = (style | WS_EX_TOOLWINDOW) & ~WS_EX_APPWINDOW
    ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)


HWND_TOPMOST = -1
SWP_NOSIZE   = 0x0001
SWP_NOMOVE   = 0x0002
SWP_NOACTIVATE = 0x0010


def snap_to_taskbar(hwnd: int, widget_w: int) -> tuple:
    """Position widget as a floating HWND_TOPMOST window at taskbar coordinates.

    No SetParent — avoids Windows 11 layering issues entirely.
    Returns (success: bool, screen_x: int, screen_y: int, taskbar_h: int).
    """
    try:
        taskbar = ctypes.windll.user32.FindWindowA(b"Shell_TrayWnd", None)
        if not taskbar:
            return False, 0, 0, 48

        tray = ctypes.windll.user32.FindWindowExA(taskbar, None, b"TrayNotifyWnd", None)
        if not tray:
            return False, 0, 0, 48

        taskbar_rect = wintypes.RECT()
        tray_rect    = wintypes.RECT()
        ctypes.windll.user32.GetWindowRect(taskbar, ctypes.byref(taskbar_rect))
        ctypes.windll.user32.GetWindowRect(tray,    ctypes.byref(tray_rect))

        taskbar_h = taskbar_rect.bottom - taskbar_rect.top
        screen_x  = tray_rect.left - widget_w
        screen_y  = taskbar_rect.top

        # Position as HWND_TOPMOST at taskbar screen coordinates
        ctypes.windll.user32.SetWindowPos(
            hwnd, HWND_TOPMOST,
            screen_x, screen_y,
            widget_w, taskbar_h,
            SWP_NOACTIVATE | SWP_SHOWWINDOW,
        )

        return True, screen_x, screen_y, taskbar_h
    except Exception:
        return False, 0, 0, 48


def get_taskbar_position(widget_w: int) -> tuple:
    """Return (screen_x, screen_y, taskbar_h) for snapping to taskbar.

    Used for periodic repositioning without touching win32 styles.
    """
    try:
        taskbar = ctypes.windll.user32.FindWindowA(b"Shell_TrayWnd", None)
        tray    = ctypes.windll.user32.FindWindowExA(taskbar, None, b"TrayNotifyWnd", None)
        taskbar_rect = wintypes.RECT()
        tray_rect    = wintypes.RECT()
        ctypes.windll.user32.GetWindowRect(taskbar, ctypes.byref(taskbar_rect))
        ctypes.windll.user32.GetWindowRect(tray,    ctypes.byref(tray_rect))
        return (
            tray_rect.left - widget_w,
            taskbar_rect.top,
            taskbar_rect.bottom - taskbar_rect.top,
        )
    except Exception:
        return None
