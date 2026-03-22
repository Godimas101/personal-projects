# Claude Usage Monitor

A lightweight Windows system tray + overlay widget that displays Claude Code usage at a glance — styled after the amber phosphor terminals of the Aliens franchise.

> **Status: Feature-complete. In personal soak testing before public release.**

---

## What It Does

- Floating overlay widget near the system clock — always visible, draggable
- Compact taskbar widget that sits flush against the Windows taskbar
- System tray icon showing current session % at a glance
- Pauses polling automatically when the screen is locked or screensaver is active
- Hides the taskbar widget when a fullscreen app or game is running
- Opens a full stats + settings panel via right-click on the tray icon

---

## Features

### Floating Widget
- Draggable amber overlay, always on top, positioned near the clock
- SESSION (5H) and WEEKLY (7D) usage bars with percentage labels
- Depleting time line above each bar — green while time remains, dims as the window expires
- Vertical pip cursor anchored to the right edge of the highest filled pip
- Blinking LIVE / PAUSED status indicator
- Position saved between sessions

### Taskbar Widget
- Compact strip that lives at the right end of the Windows taskbar
- SESSION and WEEKLY bars with percentages
- Same timer lines and pip cursors as the floating widget
- Auto-hides when a fullscreen app (game, video, presentation) is in the foreground
- Briefly flickers when the system tray hidden-icons flyout opens — cosmetic only, not fixable without WinEvent hooks

### System Tray Icon
- Amber dot in the notification area showing current session % as a number
- Right-click menu: toggle floating widget, toggle taskbar widget, open settings, exit
- Checkmarks reflect actual widget state, updated in real time

### Options Panel — General Tab
- Poll frequency (1 min → 1 hour)
- Launch on Windows startup toggle
- Use Colours toggle — switches all widgets and the panel between amber phosphor and greyscale
- Version, credits, repository link

### Options Panel — Nerds Only Tab
- All rate limit windows with mini progress bars and reset countdowns
- Today: messages, output tokens, input tokens, cache read/write, cost (USD)
- Session (current 5H block): messages, tokens, cost
- All time: totals, cost, first session date
- Burn rate: tokens/min + velocity indicator (IDLE / SLOW / NORMAL / FAST / VERY FAST)
- Model breakdown: usage % per model
- Refresh button
- Claude Code mascot

---

## Screen Lock / Screensaver Handling

The original motivation: most existing monitors keep polling when the Windows desktop is unavailable, causing freezes or crashes on screen unlock.

This tool detects both lock states via Win32 API with no extra dependencies:
- **Screen lock:** `OpenInputDesktop()` returns NULL when workstation is locked
- **Screensaver:** `SystemParametersInfo(SPI_GETSCREENSAVERRUNNING)`

While either is active, polling is fully suspended. On unlock/wake the next lightweight check fires an immediate data refresh. The widget wakes up cleanly every time.

All three major reference repos have zero screen lock handling. This is our key differentiator.

---

## Windows 11 Taskbar Note

Windows 11's taskbar uses WinUI3/XAML rendering. True Win32 `SetParent` embedding technically works at the API level but the XAML compositor paints over any embedded child windows, making them invisible. COM deskband embedding also requires third-party tools (ExplorerPatcher, StartAllBack) to work on Windows 11.

Our approach: position the taskbar widget as a `HWND_TOPMOST` floating window at exact taskbar screen coordinates, bottom-anchored, re-asserted every 300ms. Visually identical to true embedding. No third-party tools required.

---

## Data Sources

| Data | Source |
|------|--------|
| 5-hour and 7-day rate limits + reset countdowns | Anthropic OAuth API (`/api/oauth/usage`) |
| Session history, token counts, cost | Local JSONL at `~/.claude/projects/**/*.jsonl` |

No separate API key needed — reads existing Claude Code credentials from `~/.claude/.credentials.json`. Attempts a token refresh via `claude.cmd` if the token is expired.

---

## Installation

```
pip install -r requirements.txt
pythonw main.py
```

Settings are stored at `%APPDATA%\ClaudeUsageMonitor\settings.json`.

---

## Reference Projects

| Repo | Notes |
|------|-------|
| [CodeZeno/Claude-Code-Usage-Monitor](https://github.com/CodeZeno/Claude-Code-Usage-Monitor) | Rust, Win32 native, true taskbar embedding via `WS_EX_LAYERED` + `UpdateLayeredWindow` |
| [Bortlesboat/claude-usage-monitor](https://github.com/Bortlesboat/claude-usage-monitor) | Python, OAuth API + JSONL, most advanced stats |
| [Maciek-roboblog/Claude-Code-Usage-Monitor](https://github.com/Maciek-roboblog/Claude-Code-Usage-Monitor) | Python, Rich terminal UI, JSONL only |
| [amnweb/yasb](https://github.com/amnweb/yasb) | Python status bar, same TOPMOST float approach for Win11 |
| [srwi/EverythingToolbar](https://github.com/srwi/EverythingToolbar) | C#/WPF, confirms deskband doesn't work on Win11 without ExplorerPatcher |

---

## Authors

- Chris Carpenter
- Claude Sonnet 4.6 (Anthropic)
