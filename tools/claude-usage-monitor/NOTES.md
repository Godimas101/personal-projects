# Claude Usage Monitor — Dev Notes

---

## 2026-03-20 — Project Start + Technical Research

### Why we're building this
Tried CodeZeno (Rust tray widget) and Bortlesboat (Python tray widget). Both are tray-icon only — you have to hunt for the icon, hover, read a tooltip. Not visual enough.
CodeZeno had a screen-lock bug that made it unreliable. Bortlesboat replaced it but same visual problem.
Goal: a proper always-visible widget sitting next to the taskbar clock, with real progress bars and colours.

---

### Reference repos

| Repo | Language | Notes |
|------|----------|-------|
| [CodeZeno](https://github.com/CodeZeno/Claude-Code-Usage-Monitor) | Rust | Win32 taskbar embedding — sits literally inside the taskbar as a child window. Most faithful "next to the clock" implementation. |
| [Maciek-roboblog](https://github.com/Maciek-roboblog/Claude-Code-Usage-Monitor) | Python | Tray widget, basic stats |
| [Bortlesboat](https://github.com/Bortlesboat/claude-usage-monitor) | Python | Most advanced — OAuth API + JSONL, CLI mode, colour-coded icon. Currently installed at v3.1.0. |

---

### How CodeZeno positions next to the clock (Rust/Win32)

1. `FindWindowA("Shell_TrayWnd")` — gets the taskbar handle
2. `FindWindowExA(taskbar, "TrayNotifyWnd")` — gets the notification/clock area
3. `GetWindowRect(tray_wnd)` — reads its screen coordinates
4. `SetParent(widget_hwnd, taskbar_hwnd)` — re-parents widget as a taskbar child
5. `SetWindowLong()` — removes `WS_POPUP`, adds `WS_CHILD | WS_CLIPCHILDREN`
6. Positions widget at `tray_left - widget_width` (just left of the clock)
7. Uses `UpdateLayeredWindow()` for alpha-blended rendering

**For Python:** Can't easily do `SetParent` re-parenting via tkinter. Plan instead:
- Use `ctypes` to call `FindWindowA` + `GetWindowRect` to get the clock position
- Position our `overrideredirect` topmost window just above/left of that rect
- Re-query on `WM_TASKBARPOS` or a timer in case taskbar moves
- Result: floats very close to the clock rather than embedded in it — visually identical to the user

---

### Screen lock / screensaver detection (Python + ctypes, no pywin32 needed)

```python
import ctypes

def is_screensaver_active() -> bool:
    active = ctypes.c_bool()
    # SPI_GETSCREENSAVERRUNNING = 0x0072
    ctypes.windll.user32.SystemParametersInfoA(0x0072, 0, ctypes.byref(active), 0)
    return active.value

def is_workstation_locked() -> bool:
    # OpenInputDesktop returns NULL when locked or screensaver is active
    hDesk = ctypes.windll.user32.OpenInputDesktop(0, False, 0x0100)
    if hDesk:
        ctypes.windll.user32.CloseDesktop(hDesk)
        return False
    return True

def should_pause() -> bool:
    return is_screensaver_active() or is_workstation_locked()
```

Poll loop checks `should_pause()` before each update. If paused, skip the API call and reschedule. On resume, update immediately.

---

### Data sources (confirmed from Bortlesboat source)

- **Rate limits (5h / 7d):** Anthropic OAuth API
  - Credentials: `~/.claude/.credentials.json` (created by Claude Code on sign-in)
  - No separate API key needed
- **Session history / token counts:** `~/.claude/projects/**/*.jsonl`
  - Each JSONL file = one project conversation
  - Each line = one turn with token usage fields

Stats available:
- `messages` — count of conversation turns
- `input_tokens` — tokens sent to Claude
- `output_tokens` — tokens received from Claude
- `cache_creation_input_tokens` — tokens written to cache
- `cache_read_input_tokens` — tokens read from cache
- Aggregable over: current session, today, this period, all time
- Rate limits: 5-hour %, 7-day %, reset countdowns
- Budget: total token budget, used, remaining, daily burn rate

---

### Technology decisions

| Decision | Choice | Reason |
|----------|--------|--------|
| Language | Python 3 | Consistent with other personal tools, fast iteration |
| UI framework | tkinter + canvas | No external deps, full control over rendering for the aesthetic |
| Win32 access | ctypes (stdlib) | No pywin32 needed — keeps install simple |
| Packaging | PyInstaller (later) | Single `.exe` for easy startup registration |

---

### Aesthetic direction

Weyland-Yutani amber phosphor terminal (Aliens franchise). See `STYLE_GUIDE.md`.
Key: amber on near-black, chunky monospace, box-drawing borders, segmented progress bars, all-caps labels.

---

### Planned file structure

```
claude-usage-monitor/
├── main.py           — entry point, startup registration
├── widget.py         — main taskbar widget window
├── options.py        — options/stats panel (tabbed)
├── usage_reader.py   — reads JSONL files + OAuth API
├── win_utils.py      — Win32 positioning, screen lock detection
├── theme.py          — all colour/font/style constants
├── STYLE_GUIDE.md
├── NOTES.md
└── README.md
```

---

## Session Log

| Date | Work Done |
|------|-----------|
| 2026-03-20 | Project created, requirements defined, reference repos researched, technical decisions made |
