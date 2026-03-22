# Claude Usage Monitor — Dev Notes

---

## THE BUG WE ARE FIXING

**The original CodeZeno widget crashed or froze on screen unlock.**

Root cause: it kept polling the Anthropic API while the Windows desktop was unavailable (workstation locked, screensaver active). When the user returned and unlocked, the widget was in a broken state requiring a kill and restart.

**Our fix:** Before every poll, call `should_pause()`. If `True`, skip the API call entirely and reschedule a lightweight check in 10 seconds. The moment the screen is unlocked and `should_pause()` returns `False`, the next check fires an immediate data refresh. The widget wakes up cleanly every time.

This is implemented in `win_utils.py` using two Win32 calls — no pywin32, no external dependencies:

```python
def is_screensaver_active() -> bool:
    active = ctypes.c_bool()
    ctypes.windll.user32.SystemParametersInfoA(0x0072, 0, ctypes.byref(active), 0)
    return active.value

def is_workstation_locked() -> bool:
    hDesk = ctypes.windll.user32.OpenInputDesktop(0, False, 0x0100)
    if hDesk:
        ctypes.windll.user32.CloseDesktop(hDesk)
        return False
    return True

def should_pause() -> bool:
    return is_screensaver_active() or is_workstation_locked()
```

**All three reference repos (CodeZeno, Bortlesboat, Maciek) have zero screen lock handling. This is our key differentiator.**

---

## 2026-03-20 — Project Start + Full Technical Research

### Why we're building this
Tried CodeZeno (Rust taskbar widget) and Bortlesboat (Python tray widget). Both are tray-icon only.
CodeZeno had a screen-lock bug. Bortlesboat replaced it but same visual problem — you hunt for an icon.
Goal: a proper always-visible widget next to the taskbar clock, with real progress bars and colours you can actually see.

---

### Reference Repos — Full Analysis

#### CodeZeno/Claude-Code-Usage-Monitor (Rust)
**Type:** Native Win32 application, embeds directly inside the Windows taskbar

**How it positions next to the clock:**
1. `FindWindowW("Shell_TrayWnd")` — taskbar handle
2. `FindWindowExW(taskbar, "TrayNotifyWnd")` — notification/clock area
3. `SHAppBarMessage(ABM_GETTASKBARPOS)` — taskbar position via APPBARDATA
4. `SetParent(widget_hwnd, taskbar_hwnd)` — re-parents widget as taskbar child
5. Strips `WS_POPUP`, adds `WS_CHILD | WS_CLIPSIBLINGS`
6. Positions at `tray_left - widget_width` (just left of the clock)
7. `UpdateLayeredWindow()` for alpha-blended rendering

**Window styles:**
- `WS_EX_TOOLWINDOW` — hides from taskbar app list
- `WS_EX_LAYERED` — alpha blending
- `WS_EX_NOACTIVATE` — doesn't steal focus on click

**Data source:** OAuth API
- Endpoint: `GET https://api.anthropic.com/api/oauth/usage`
- Header: `Authorization: Bearer {token}`, `anthropic-beta: oauth-2025-04-20`
- Credentials from: `~/.claude/.credentials.json` → `claudeAiOauth.accessToken`
- Fallback: POST to `/v1/messages`, read `anthropic-ratelimit-unified-5h-utilization` headers
- Token refresh: shells out to `claude.cmd -p .`

**Stats available:** 5-hour %, 7-day %, reset countdowns

**Settings:** `%APPDATA%\ClaudeCodeUsageMonitor\settings.json` (`tray_offset`, `poll_interval_ms`, `language`)

**Screen lock detection:** None

**Other features:** DPI awareness, theme detection (registry), update checker, multi-language, single-instance mutex

---

#### Bortlesboat/claude-usage-monitor (Python, v3.1.0) — currently installed
**Type:** System tray icon + popup dashboard

**Data source:** OAuth API + local JSONL
- Same endpoint as CodeZeno: `GET https://api.anthropic.com/api/oauth/usage`
- JSONL files: `~/.claude/projects/**/*.jsonl`
- Parsed JSONL fields: `input_tokens`, `output_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens` — per model

**Rate limit windows tracked:**
- 5-Hour, 7-Day, 7-Day Opus, 7-Day Sonnet, 7-Day OAuth Apps, 7-Day Cowork, Extra Usage

**Stats available:**
- Today: messages, output tokens, sessions
- Current period: messages, output tokens, sessions
- All-time: totals, days active, sessions
- Budget: utilization %, daily budget, days remaining, projected %
- Notifications at 80% and 90% thresholds

**Screen lock detection:** None — polls every 60 seconds regardless

---

#### Maciek-roboblog/Claude-Code-Usage-Monitor (Python, Rich terminal)
**Type:** Terminal UI (not a widget — full terminal app using Rich library)

**Data source:** Local JSONL only — no API calls
- JSONL paths: `~/.claude/projects` or `~/.config/claude/projects`
- Fields: input tokens, output tokens, cache creation tokens, cache read tokens — per model

**Stats available (best in class for depth):**
- Burn rate: tokens/minute, cost/hour
- P90 percentile predictions (when will you hit your limit)
- Velocity: Slow / Normal / Fast / Very Fast
- Per-model breakdown: Opus %, Sonnet % of total usage
- USD cost tracking per session + projected daily cost
- Session block organisation (5-hour windows with gap detection)
- Rate limit event detection (identifies when limits were hit)
- Daily/monthly aggregation views

**Screen lock detection:** None

---

### Screen Lock Detection — Our Differentiator
All three existing tools have zero screen lock or screensaver handling. This is the bug that caused the original problem.

**Implementation plan (Python + ctypes, no pywin32 needed):**
```python
import ctypes

def is_screensaver_active() -> bool:
    active = ctypes.c_bool()
    ctypes.windll.user32.SystemParametersInfoA(0x0072, 0, ctypes.byref(active), 0)
    return active.value

def is_workstation_locked() -> bool:
    hDesk = ctypes.windll.user32.OpenInputDesktop(0, False, 0x0100)
    if hDesk:
        ctypes.windll.user32.CloseDesktop(hDesk)
        return False
    return True

def should_pause() -> bool:
    return is_screensaver_active() or is_workstation_locked()
```

---

### Taskbar Positioning — Python Approach
CodeZeno does proper Win32 `SetParent` embedding (Rust only, not practical from Python/tkinter).
Our Python plan:
- `ctypes.windll.user32.FindWindowA(b"Shell_TrayWnd", None)` — taskbar
- `ctypes.windll.user32.FindWindowExA(taskbar, None, b"TrayNotifyWnd", None)` — clock area
- `ctypes.windll.user32.GetWindowRect(tray, byref(rect))` — get position
- Float `overrideredirect` window just above/left of that rect
- Re-query on a timer in case taskbar moves
- Set `WS_EX_TOOLWINDOW` via ctypes to hide from taskbar app list

Result: floats very close to the clock. Visually identical to the user — not embedded, but indistinguishable.

---

### Data Sources — Final Plan
| Data | Source |
|------|--------|
| 5-hour rate limit % + reset | OAuth API (`/api/oauth/usage`) |
| 7-day rate limit % + reset | OAuth API |
| Model-specific limits | OAuth API (7-Day Opus, 7-Day Sonnet, etc.) |
| Session token counts | JSONL files (`~/.claude/projects/**/*.jsonl`) |
| Burn rate, velocity, P90 | Calculated from JSONL |
| Cost in USD | Calculated from JSONL + hardcoded model pricing |

---

### Stats to Show — Planned

**Widget (always visible):**
- Current session % of 5-hour limit
- Weekly % of 7-day limit
- Reset countdown

**Stats Tab (options panel):**
- All rate limit windows (5h, 7d, Opus, Sonnet)
- Today: messages, input/output/cache tokens
- This period: same
- All-time: same + days active, sessions
- Burn rate (tokens/min)
- Velocity indicator
- Per-model breakdown
- Budget: %, daily burn, days remaining
- USD cost (session + projected)

---

### Technology Decisions

| Decision | Choice | Reason |
|----------|--------|--------|
| Language | Python 3 | Fast iteration, familiar, no compile step |
| UI framework | tkinter + canvas | Full rendering control for the aesthetic, no extra deps |
| Win32 access | ctypes (stdlib) | No pywin32 needed |
| HTTP | urllib or requests | Keep deps minimal |
| Packaging | PyInstaller (later) | Single `.exe` for startup registration |

---

### Actual File Structure (as built)
```
claude-usage-monitor/
├── main.py           — entry point, single-instance mutex, load/save settings to %APPDATA%\ClaudeUsageMonitor\settings.json
├── widget.py         — main widget: tries taskbar embedding, falls back to floating; horizontal/vertical layouts
├── options.py        — options panel: GENERAL tab + NERDS ONLY tab (2-col fixed layout, no scroll)
├── usage_reader.py   — OAuth API (fetch_rate_limits), JSONL parser (scan_local), model pricing, RateLimitData, LocalStats
├── win_utils.py      — screen lock detection (should_pause), taskbar helpers, set_tool_window, embed_in_taskbar
├── theme.py          — colour constants, best_font(), draw_bar(), draw_scanlines(), draw_bevel(), usage_colour(), fmt_*
├── STYLE_GUIDE.md
├── NOTES.md
└── README.md
```

---

### Windows 11 Taskbar — Why True Embedding Doesn't Work

**Windows 11's taskbar is WinUI3/XAML, not Win32 GDI.**
(Source: [ramensoftware/windows-11-taskbar-styling-guide](https://github.com/ramensoftware/windows-11-taskbar-styling-guide))

The taskbar renders via a XAML compositor layer on top of any Win32 child windows. `SetParent` into `Shell_TrayWnd` technically succeeds at the API level — the window IS embedded — but the XAML render layer paints over it. This is why our widget was invisible despite all Win32 calls returning success.

**COM Deskband doesn't work on vanilla Windows 11 either.**
(Source: [srwi/EverythingToolbar](https://github.com/srwi/EverythingToolbar))

EverythingToolbar explicitly recommends the Launcher (non-embedded) approach for Windows 11. Deskband (COM toolbar) only works with ExplorerPatcher or StartAllBack installed — third-party tools that replace the taskbar with a classic Win32 one.

**Our solution: HWND_TOPMOST floating window at taskbar screen coordinates.**
Position the widget at `(tray_left - widget_w, taskbar_top)` as a `HWND_TOPMOST` / `overrideredirect` window. Re-assert topmost + reposition every 2 seconds to survive focus changes. This is visually identical to true embedding and works reliably on Windows 11.

**YASB** ([amnweb/yasb](https://github.com/amnweb/yasb)) takes the same general approach — a Python-based always-on-top overlay bar rather than true taskbar embedding.

---

### Taskbar Widget — Final Implementation (HWND_TOPMOST float)

`SetParent` into the taskbar was abandoned — see "Windows 11 Taskbar" section above.

**`win_utils.get_taskbar_position(widget_w)`:**
1. `FindWindowA("Shell_TrayWnd")` → taskbar HWND
2. `FindWindowExA(taskbar, "TrayNotifyWnd")` → clock/tray area
3. `GetWindowRect` on both → `screen_x = tray_left - widget_w`, `taskbar_top`, `taskbar_h`
4. Returns `(screen_x, taskbar_top, taskbar_h)`

**`TaskbarWidget._reposition()`:**
- `embed_h = taskbar_h - 1` (leaves 1px of taskbar visible at top)
- `y = taskbar_top + taskbar_h - embed_h` — bottom-anchored
- `win.geometry(f"{W_EMBED}x{embed_h}+{screen_x}+{y}")`
- Re-runs every 300ms via `_topmost_loop` which also re-asserts `HWND_TOPMOST`

**Fullscreen detection in `_topmost_loop`:**
- `win_utils.is_fullscreen()` — checks `SHQueryUserNotificationState` (states 3/4 = D3D/presentation)
  plus foreground window rect ≥ screen dimensions (borderless fullscreen games)
- Widget hides itself when fullscreen; unhides when fullscreen ends

**Taskbar layout (W=260, H=taskbar_h-1):**
```
● CLAUDE | 5H ▓▓▓▓▓░░░░░ 61% | 7D ▓▓░░░░░░░░ 20%
```
- Constants: `VSEP_1=66`, `VSEP_2=163`, `BAR_W_E=48`, `BAR_SEGS_E=10`

---

### Options Panel — Nerds Only tab (2-column fixed layout)

No scrollbar. Window auto-sizes to fit Nerds Only content on first open, then locks size.

**Left column:** RATE LIMITS (all API windows with mini-bars), BURN RATE (tok/min + velocity), MODEL BREAKDOWN

**Right column:** TODAY (messages/output/input/cache/cost), SESSION (5H block), ALL TIME

**Sizing trick:** in `_build()`, temporarily switches to Nerds Only tab, calls `update_idletasks()`, reads `winfo_reqwidth/height`, locks geometry, then switches back to General tab.

**Panel positioning:** Uses `winfo_rootx()/rooty()` (not `winfo_x/y`) so it works correctly when the widget is embedded in the taskbar. Opens above the widget; falls back to below if off-screen.

---

### Known Bugs Fixed

| Bug | Fix |
|-----|-----|
| `TypeError: float() argument... NoneType` | API returns `"utilization": null` for some windows. Fixed: `float(raw.get("utilization") or 0)` in `WindowData.__init__` |
| Widget invisible after launch | `main.py` had `root.withdraw()` before widget built. Fixed: removed `withdraw()` entirely |
| Single-instance mutex blocking re-launch after crash | Background thread crash left main thread's mutex held. Fixed: kill stuck PID via `Stop-Process` |

---

## Session Log

| Date | Work Done |
|------|-----------|
| 2026-03-20 | Project created, all three reference repos researched, aesthetic research completed, technical decisions made, NOTES + README + STYLE_GUIDE written |
| 2026-03-20 | Built all 6 source files. Fixed 3 startup bugs. Widget working as floating amber phosphor widget. |
| 2026-03-20 | Upgraded to true taskbar embedding via Win32 SetParent (embed_in_taskbar in win_utils.py). Rewrote widget.py with dual floating/embedded layouts. Rewrote options.py Nerds Only tab as 2-column fixed-size layout without scrollbar. Pending: reboot test to verify taskbar embedding works. |
| 2026-03-21 | Discovered Windows 11 taskbar is WinUI3/XAML — SetParent embeds correctly at Win32 level but XAML layer paints over it. Switched to HWND_TOPMOST float-at-taskbar-coordinates approach. Added system tray icon (pystray, amber dot) with toggle menu for floating/taskbar widgets. Refactored widget.py into FloatingWidget + TaskbarWidget classes. Fixed vanish-on-options-close bug by re-asserting topmost every 300ms in reposition loop. Both widgets now working. |
| 2026-03-21 | Fixed screen-unlock 0% bug (failed fetch no longer overwrites good data). Added fullscreen detection (SHQueryUserNotificationState + foreground rect check) — taskbar widget hides during games/fullscreen apps. Fixed tray checkmark timing bug (threading.Timer delay before update_menu). Added depleting time lines above usage bars (green→dim amber) and vertical pip-edge cursors anchored to highest filled pip. Removed session countdown text and gear buttons from both widgets. Tray icon now renders current session % as text on the amber dot. Fixed timer line and cursor widths to match exact draw_bar integer math (bar_actual_width, bar_pip_edge). Narrowed floating widget from 262→224px for equal left/right margins. LIVE/PAUSED status text aligned to percentage column, bumped to header font size. Options General tab: LAUNCH ON STARTUP moved to label column. Added USE COLOURS toggle — live greyscale mode via set_use_colours() in theme.py, rebuilds options panel in place. Added Claude Code mascot ASCII art to Nerds Only left column. |
