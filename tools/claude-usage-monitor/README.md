# Claude Usage Monitor

A lightweight Windows taskbar widget that displays Claude Code usage at a glance — styled after the amber phosphor terminals of the Aliens franchise.

> **Status: Work in progress — not yet ready for public release.**

---

## What It Does

- Sits inside the Windows taskbar, just left of the system clock
- Shows current session and weekly usage as visual progress bars
- System tray icon with toggle controls for each widget
- Pauses polling automatically when the screen is locked or screensaver is active — resumes on wake/unlock
- Opens a full stats + settings panel on right-click

---

## Features

### Taskbar Widget
- Compact strip that lives permanently in the taskbar, left of the clock
- Session (5H) and weekly (7D) usage bars with percentages
- Amber phosphor / Weyland-Yutani terminal aesthetic
- Stays visible through system tray flyouts and focus changes

### Floating Widget
- Draggable overlay window positioned near the clock
- Full session + weekly bars with percentage and reset countdown
- LIVE / PAUSED status indicator

### System Tray Icon
- Always-present amber dot in the notification area
- Right-click menu: toggle floating widget on/off, toggle taskbar widget on/off, open settings, exit

### Options Panel — General Tab
- Poll frequency setting
- Launch on Windows startup toggle
- Version, credits, repository link

### Options Panel — Nerds Only Tab
- All rate limit windows with progress bars and reset countdowns
- Today: messages, output tokens, input tokens, cache read/write, cost
- Session (5H block): messages, tokens, cost
- All time: totals, cost, first session date
- Burn rate: tokens/min + velocity indicator
- Model breakdown: usage % per model
- Refresh button

---

## Screen Lock / Screensaver Handling

The bug that motivated building this: most existing monitors keep polling when the Windows desktop is unavailable, causing freezes or crashes on screen unlock.

This tool detects both lock states via Win32 API with no extra dependencies:
- **Screen lock:** `OpenInputDesktop()` returns NULL when workstation is locked
- **Screensaver:** `SystemParametersInfo(SPI_GETSCREENSAVERRUNNING)`

While either is active, the poll timer is fully suspended. It resumes automatically on unlock/wake.

All three major reference repos have zero screen lock handling. This is our key differentiator.

---

## Windows 11 Taskbar Note

Windows 11's taskbar uses WinUI3/XAML rendering. True Win32 `SetParent` embedding technically works at the API level but the XAML layer paints over any embedded child windows — making them invisible. COM deskband embedding also requires third-party tools (ExplorerPatcher, StartAllBack) to work on Windows 11.

Our approach: position the taskbar widget as a `HWND_TOPMOST` floating window at exact taskbar screen coordinates, bottom-anchored. Visually identical to true embedding. No third-party tools required.

---

## Data Sources

| Data | Source |
|------|--------|
| 5-hour and 7-day rate limits + reset countdowns | Anthropic OAuth API (`/api/oauth/usage`) |
| Session history, token counts, cost | Local JSONL at `~/.claude/projects/**/*.jsonl` |

No separate API key needed — reads existing Claude Code credentials from `~/.claude/.credentials.json`.

---

## Installation

```
pip install -r requirements.txt
python main.py
```

---

## Reference Projects

| Repo | Notes |
|------|-------|
| [CodeZeno/Claude-Code-Usage-Monitor](https://github.com/CodeZeno/Claude-Code-Usage-Monitor) | Rust, Win32 native window, layered rendering — taskbar embedding works because it uses `WS_EX_LAYERED` + `UpdateLayeredWindow` |
| [Bortlesboat/claude-usage-monitor](https://github.com/Bortlesboat/claude-usage-monitor) | Python, OAuth API + JSONL, most advanced stats |
| [Maciek-roboblog/Claude-Code-Usage-Monitor](https://github.com/Maciek-roboblog/Claude-Code-Usage-Monitor) | Python, Rich terminal UI, JSONL only |
| [amnweb/yasb](https://github.com/amnweb/yasb) | Python status bar, same TOPMOST float approach for Win11 |
| [srwi/EverythingToolbar](https://github.com/srwi/EverythingToolbar) | C#/WPF, confirms deskband doesn't work on Win11 without ExplorerPatcher |

---

## Authors

- Chris Carpenter
- Claude Sonnet 4.6 (Anthropic)
