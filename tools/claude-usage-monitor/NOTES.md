# Claude Usage Monitor — Dev Notes

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

### Planned File Structure
```
claude-usage-monitor/
├── main.py           — entry point, startup registration
├── widget.py         — main taskbar widget window
├── options.py        — options/stats panel (tabbed)
├── usage_reader.py   — JSONL parser + OAuth API calls
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
| 2026-03-20 | Project created, all three reference repos researched, aesthetic research completed, technical decisions made, NOTES + README + STYLE_GUIDE written |
