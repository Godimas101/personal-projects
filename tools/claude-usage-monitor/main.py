# main.py — Entry point

import json
import os
import pathlib
import sys
import tkinter as tk

# ── Settings ──────────────────────────────────────────────────────────────────

APPDATA_DIR   = pathlib.Path(os.environ.get("APPDATA", pathlib.Path.home())) / "ClaudeUsageMonitor"
SETTINGS_FILE = APPDATA_DIR / "settings.json"

DEFAULT_SETTINGS = {
    "poll_interval_ms": 15 * 60 * 1000,
    "position":         None,
    "show_floating":    True,
    "show_taskbar":     True,
}


def load_settings() -> dict:
    try:
        with open(SETTINGS_FILE, encoding="utf-8") as f:
            data = json.load(f)
        return {**DEFAULT_SETTINGS, **data}
    except Exception:
        return dict(DEFAULT_SETTINGS)


def save_settings(settings: dict) -> None:
    try:
        APPDATA_DIR.mkdir(parents=True, exist_ok=True)
        saveable = {k: v for k, v in settings.items() if not k.startswith("_")}
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(saveable, f, indent=2)
    except Exception:
        pass


# ── Single instance guard ─────────────────────────────────────────────────────

def _acquire_lock() -> bool:
    try:
        import ctypes
        mutex = ctypes.windll.kernel32.CreateMutexW(
            None, True, "Global\\ClaudeUsageMonitor"
        )
        return ctypes.windll.kernel32.GetLastError() != 183  # ERROR_ALREADY_EXISTS
    except Exception:
        return True


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if not _acquire_lock():
        sys.exit(0)

    settings = load_settings()

    import theme as T
    T.apply_theme(settings.get("theme", "Default"))

    root = tk.Tk()
    root.overrideredirect(True)  # no decorations, no taskbar button
    root.withdraw()  # invisible owner window — keeps mainloop alive

    import widget as W
    import tray   as Tr

    floating = None
    taskbar  = None

    # ── Create initial widgets ─────────────────────────────────────────────────

    if settings.get("show_floating", True):
        floating = W.FloatingWidget(root, settings)

    if settings.get("show_taskbar", True):
        taskbar = W.TaskbarWidget(root, settings)

    # ── Toggle callbacks (called from tray menu, already dispatched to main thread) ──

    def toggle_floating():
        nonlocal floating
        if floating:
            floating.destroy()
            floating = None
            settings["show_floating"] = False
        else:
            settings["show_floating"] = True
            floating = W.FloatingWidget(root, settings)
        save_settings(settings)

    def toggle_taskbar():
        nonlocal taskbar
        if taskbar:
            taskbar.destroy()
            taskbar = None
            settings["show_taskbar"] = False
        else:
            settings["show_taskbar"] = True
            taskbar = W.TaskbarWidget(root, settings)
        save_settings(settings)

    def open_settings():
        target = floating or taskbar
        if target:
            target._open_options()

    def on_exit():
        save_settings(settings)
        root.after(0, root.destroy)

    # ── Tray icon ──────────────────────────────────────────────────────────────

    tray = Tr.Tray(settings, {
        "toggle_floating": lambda: root.after(0, toggle_floating),
        "toggle_taskbar":  lambda: root.after(0, toggle_taskbar),
        "settings":        lambda: root.after(0, open_settings),
        "exit":            on_exit,
    })
    tray.start()
    settings["_on_data_cb"] = lambda rate, local: tray.update_usage(rate, local)

    def on_colour_change():
        if floating:
            floating._redraw()
        if taskbar:
            taskbar._redraw()
    settings["_on_colour_change_cb"] = on_colour_change

    try:
        root.mainloop()
    finally:
        save_settings(settings)
        tray.stop()


if __name__ == "__main__":
    main()
