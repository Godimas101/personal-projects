# Claude Usage Monitor

A lightweight Windows taskbar widget that displays Claude Code usage at a glance — styled after the amber phosphor terminals of the Aliens franchise.

---

## What It Does

- Floats next to the Windows taskbar clock (right side, above the system tray)
- Shows current session usage and weekly usage as visual progress bars
- Pauses polling automatically when the screen is locked or a screensaver is active — resumes on wake/unlock
- Opens a full stats + settings panel on click

---

## Features

### Widget
- Current session usage bar + percentage
- Weekly usage bar + percentage
- Compact — designed to live permanently next to the clock
- Draggable for fine repositioning
- Amber phosphor / Weyland-Yutani terminal aesthetic

### Options Panel — General Tab
- Poll frequency setting (how often the widget checks and updates)
- Launch on Windows startup toggle
- Link to this repository
- Version number
- Credits (Chris Carpenter + Claude Sonnet 4.6)

### Options Panel — Stats Tab
- Full usage breakdown: messages, input tokens, output tokens, cache tokens
- Session / daily / period / all-time stats
- Rate limit countdowns (5-hour and 7-day reset timers)
- Budget remaining and daily burn rate

---

## Screen Lock / Screensaver Handling

The bug that motivated building this: most existing monitors keep polling when the Windows desktop is unavailable, causing freezes or crashes on screen unlock.

This tool detects both lock states via Win32 API with no extra dependencies:
- **Screen lock:** `OpenInputDesktop()` returns NULL when workstation is locked
- **Screensaver:** `SystemParametersInfo(SPI_GETSCREENSAVERRUNNING)`

While either is active, the poll timer is fully suspended. It resumes automatically on unlock/wake.

---

## Data Sources

- **Rate limit data:** Anthropic OAuth API — no extra key needed, reads existing Claude Code credentials from `~/.claude/.credentials.json`
- **Session history:** Local JSONL files at `~/.claude/projects/**/*.jsonl`

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
| [CodeZeno/Claude-Code-Usage-Monitor](https://github.com/CodeZeno/Claude-Code-Usage-Monitor) | Rust, Win32 taskbar embedding — the gold standard for positioning |
| [Maciek-roboblog/Claude-Code-Usage-Monitor](https://github.com/Maciek-roboblog/Claude-Code-Usage-Monitor) | Python tray widget |
| [Bortlesboat/claude-usage-monitor](https://github.com/Bortlesboat/claude-usage-monitor) | Python, most advanced stats, OAuth API + JSONL, v3.1.0 |

---

## Authors

- Chris Carpenter
- Claude Sonnet 4.6 (Anthropic)
