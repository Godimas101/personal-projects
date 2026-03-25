# 🟠 Claude Usage Monitor

> **"Never be surprised by a rate limit again — unless you deserve it."**

A lightweight Windows widget that shows your Claude Code usage at a glance. Amber phosphor aesthetic. Always on top. Knows when you've locked your screen.

---

## 🚀 What It Does

- **Floating overlay** — draggable amber widget near the system clock, always visible
- **Taskbar widget** — compact strip that lives flush against the Windows taskbar
- **System tray icon** — shows current session % as a number on an amber dot
- **Smart polling** — pauses automatically when screen is locked or screensaver is active
- **Fullscreen-aware** — taskbar widget hides itself when a game or fullscreen app is running
- **Right-click → settings** — full stats + configuration panel

---

## 📊 What It Shows

### Floating & Taskbar Widgets
- SESSION (5H) and WEEKLY (7D) usage bars with percentage labels
- Depleting time line above each bar — green while time remains, dims as the window closes
- Vertical pip cursor anchored to the right edge of the last filled pip
- Blinking LIVE / PAUSED status

### Options Panel — General Tab
- **Tool Theme** — choose from Default (amber), Red, Blue, Green, Purple, Cyan, Orange, or White phosphor
- **Poll Interval** — 1 min to 1 hour
- **Launch on Startup** — Windows startup toggle
- Per-widget settings: **Transparent Background** and **Text F/X** (scanlines + bevel on/off)
- Version, credits, and repository link

### Options Panel — Nerds Only Tab
- All rate limit windows with mini progress bars and reset countdowns
- Today / Session / All Time: messages, tokens, cost (USD)
- Burn rate (tokens/min) + velocity indicator
- Per-model usage breakdown
- Refresh button
- Claude Code mascot

---

## 🔒 Screen Lock Handling

Most existing monitors keep polling when Windows is locked, causing freezes or stale data on unlock. This one doesn't.

Lock state is detected via Win32 API — no extra dependencies:
- **Workstation locked:** `OpenInputDesktop()` returns NULL
- **Screensaver active:** `SystemParametersInfo(SPI_GETSCREENSAVERRUNNING)`

While either is active, polling suspends entirely. On wake, the next check fires an immediate refresh. Clean every time.

---

## 🖥️ Windows 11 Taskbar Note

Windows 11's taskbar is WinUI3/XAML — `SetParent` embeds correctly at the Win32 level but the XAML compositor paints right over it. Deskband embedding also requires ExplorerPatcher or StartAllBack.

Our approach: `HWND_TOPMOST` floating window positioned at exact taskbar screen coordinates, re-asserted every 300ms. Visually identical to true embedding, no third-party tools required.

---

## 📡 Data Sources

| Data | Source |
|------|--------|
| 5-hour and 7-day rate limits + reset countdowns | Anthropic OAuth API (`/api/oauth/usage`) |
| Session history, token counts, cost | Local JSONL files at `~/.claude/projects/**/*.jsonl` |

No separate API key needed — reads your existing Claude Code credentials from `~/.claude/.credentials.json`. Attempts a token refresh via `claude.cmd` if expired.

---

## 📦 Installation

```
pip install -r requirements.txt
pythonw main.py
```

Settings are stored at `%APPDATA%\ClaudeUsageMonitor\settings.json`.

---

## 🔩 Requirements

- Windows 10 / 11
- Python 3.10+
- Claude Code installed (provides credentials)

---

## 🙏 Credits & Reference Projects

Built by **Chris Carpenter** and **Claude Sonnet 4.6**.

| Repo | Notes |
|------|-------|
| [CodeZeno/Claude-Code-Usage-Monitor](https://github.com/CodeZeno/Claude-Code-Usage-Monitor) | Rust, Win32 native, true taskbar embedding |
| [Bortlesboat/claude-usage-monitor](https://github.com/Bortlesboat/claude-usage-monitor) | Python, OAuth API + JSONL, advanced stats |
| [Maciek-roboblog/Claude-Code-Usage-Monitor](https://github.com/Maciek-roboblog/Claude-Code-Usage-Monitor) | Python, Rich terminal UI, JSONL only |
| [amnweb/yasb](https://github.com/amnweb/yasb) | Python status bar, same TOPMOST float approach for Win11 |

---

## 🧡 Support

This tool is free and always will be. If it saves you from a surprise rate limit, consider supporting on Patreon — it helps keep the mods and tools coming.

[![Support on Patreon](https://raw.githubusercontent.com/Godimas101/personal-projects/main/patreon/patreon-medium.png)](https://patreon.com/Godimas101)

---

*Please poll responsibly.*
