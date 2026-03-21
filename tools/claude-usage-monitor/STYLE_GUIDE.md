# Claude Usage Monitor — Style Guide

> Weyland-Yutani terminal aesthetic. Amber phosphor on near-black.
> Cassette futurism: tactile, utilitarian, chunky, monospace.
> Inspired specifically by the MU-TH-UR 6000 computer in Aliens (1986).

---

## Aesthetic Reference

### What makes it "Aliens terminal" specifically

- **Amber phosphor**, not green. The generic hacker aesthetic is green-on-black. Weyland-Yutani is amber/orange-on-black — warmer, more industrial.
- **All caps everywhere.** Labels, values, section headers — uppercase only.
- **Box-drawing borders.** Panels are framed with `╔═╗ ║ ╚═╝` characters or canvas-drawn equivalents. Hard corners, no rounded edges.
- **Chunky segmented progress bars.** Not a smooth fill — discrete blocks: `▓▓▓▓▓░░░░░`
- **Blinking cursor / indicator.** At least one element blinks slowly (800–1000ms cycle). Signals the system is alive.
- **No decorative imagery.** Everything on screen has a function. Labels, values, bars, status. Nothing else.
- **Hierarchical data presentation.** Data grouped in labelled boxes. Hierarchy is visual and immediate.
- **Status indicators.** `● ACTIVE`, `○ IDLE`, `▶ POLLING`, `■ PAUSED` — small, left of a label.

### Cassette futurism additions

- Physical feel: elements look like they could be buttons or readouts on hardware
- Slight bevel / inset effect on panels (fake with slightly lighter/darker border pairs)
- Indicator "lights" — small filled circles that change colour (green=ok, amber=warn, red=alert)

---

## Colour Palette

| Token | Hex | Role |
|-------|-----|------|
| `BG` | `#090909` | Window background — near total black |
| `PANEL` | `#0f0e0c` | Panel/card background — barely warm |
| `BORDER_DIM` | `#2a1f0a` | Panel border lines — dark amber |
| `BORDER` | `#4a3510` | Active panel border — mid amber |
| `AMBER` | `#e8a020` | Primary text, labels — classic phosphor amber |
| `AMBER_BRIGHT` | `#ffbe3c` | Key values, percentages, highlighted data |
| `AMBER_DIM` | `#7a5010` | Secondary labels, hints, metadata |
| `AMBER_GLOW` | `#ff9900` | Accent — blinking cursor, active indicator |
| `GREEN` | `#3ddc6a` | Good state — usage low, system healthy |
| `YELLOW` | `#f0c040` | Warning state — usage moderate |
| `RED` | `#e03020` | Alert state — usage high, rate limited |
| `SCANLINE` | `#0d0c0a` | Scanline stripe colour (barely different from BG) |

```python
BG           = "#090909"
PANEL        = "#0f0e0c"
BORDER_DIM   = "#2a1f0a"
BORDER       = "#4a3510"
AMBER        = "#e8a020"
AMBER_BRIGHT = "#ffbe3c"
AMBER_DIM    = "#7a5010"
AMBER_GLOW   = "#ff9900"
GREEN        = "#3ddc6a"
YELLOW       = "#f0c040"
RED          = "#e03020"
SCANLINE     = "#0d0c0a"
```

### Usage-based colour mapping

Map usage percentage to colour:

```python
def usage_colour(pct: float) -> str:
    if pct < 0.60:  return GREEN
    if pct < 0.85:  return YELLOW
    return RED
```

---

## Typography

**All text is monospace. All text is uppercase.**

| Token | Spec | Usage |
|-------|------|-------|
| `FONT_TINY` | `("Courier New", 7)` | Status indicators, scanline labels |
| `FONT_SMALL` | `("Courier New", 8)` | Secondary labels, metadata |
| `FONT_BODY` | `("Courier New", 9)` | Standard labels, panel text |
| `FONT_VALUE` | `("Courier New", 11, "bold")` | Key numbers, percentages |
| `FONT_TITLE` | `("Courier New", 9, "bold")` | Panel titles, section headers |

Always call `.upper()` on any string before displaying it.

Alternative monospace fonts that enhance the aesthetic if installed:
- `Fixedsys` — very authentic, Windows bitmap font
- `Perfect DOS VGA 437` — free, extremely period-accurate
- `Terminus` — clean, readable, slightly modern
- `IBM Plex Mono` — modern but still terminal-feeling

Fall back to `Courier New` if preferred fonts aren't installed.

---

## UI Elements

### Progress Bar (segmented)

Draw discrete blocks, not a smooth fill. Target 10–20 segments for the widget width.

```python
FILLED_CHAR = "▓"
EMPTY_CHAR  = "░"

def render_bar(pct: float, segments: int = 16) -> str:
    filled = round(pct * segments)
    return FILLED_CHAR * filled + EMPTY_CHAR * (segments - filled)

# e.g. "▓▓▓▓▓░░░░░░░░░░░"
```

On canvas: draw filled rectangles with 1px gaps between segments, not characters.

### Panel border

Use canvas `create_rectangle` with no fill, coloured outline. For the inset/bevel effect, draw two rectangles — outer at `BORDER_DIM`, inner at `BORDER`. 1px each.

For the Aliens look, use a 1px gap between the border and content.

Box-drawing approach (tkinter Text/Label):
```
╔══════════════════════╗
║  SESSION             ║
╚══════════════════════╝
```

### Status indicator light

Small filled circle that changes colour based on state:
```python
canvas.create_oval(x, y, x+6, y+6, fill=GREEN, outline="")   # active
canvas.create_oval(x, y, x+6, y+6, fill=AMBER_DIM, outline="") # idle
canvas.create_oval(x, y, x+6, y+6, fill=RED, outline="")      # alert
```

### Blinking cursor / active indicator

A small rectangle or `▮` character that toggles visibility every 900ms:

```python
def _blink(self):
    self._cursor_visible = not self._cursor_visible
    colour = AMBER_GLOW if self._cursor_visible else BG
    self._canvas.itemconfig(self._cursor_id, fill=colour)
    self._root.after(900, self._blink)
```

### Scanline effect

Horizontal lines across the canvas at every 2px, drawn in `SCANLINE` with `stipple="gray50"` to fake transparency. Draw after all other content so they overlay everything.

```python
for y in range(0, height, 2):
    canvas.create_line(0, y, width, y, fill=SCANLINE, stipple="gray50")
```

Use sparingly — on the widget background only, not the options panel.

---

## Widget Layout (main window)

```
┌─────────────────────────────┐
│ ● CLAUDE  [settings button] │  ← header row: indicator + title + gear
├─────────────────────────────┤
│ SESSION                     │  ← section label
│ ▓▓▓▓▓░░░░░░░░░░  32%       │  ← bar + percentage
├─────────────────────────────┤
│ WEEKLY                      │
│ ▓▓▓░░░░░░░░░░░░  18%       │
├─────────────────────────────┤
│ RESETS  4H 12M              │  ← muted footer, reset countdown
└─────────────────────────────┘
```

- Total width: ~220–260px (just wide enough to read clearly)
- Total height: ~90–110px
- `overrideredirect(True)` — no window chrome
- `wm_attributes("-topmost", True)` — always on top
- No taskbar button (set `WS_EX_TOOLWINDOW` via ctypes)
- Draggable via click-drag on the header row

---

## Options Panel Layout

Standard tkinter `Toplevel` with window chrome (this one gets a title bar).

- Background: `BG`
- Border: 1px `BORDER` on all panels
- All text uppercase
- Two tabs: `GENERAL` and `STATS`
- Tab style: flat buttons, active tab has `AMBER` text and `BORDER` underline, inactive has `AMBER_DIM`

---

## Window Behaviour

| Property | Value |
|----------|-------|
| Widget background | `BG` |
| Widget border | None (overrideredirect) |
| Always on top | Yes |
| Taskbar button | No (`WS_EX_TOOLWINDOW`) |
| Opacity | 1.0 (fully opaque) |
| Draggable | Yes (click + drag anywhere on widget) |
| Right-click | Opens options panel |
| Left-click | Toggles stats tooltip or opens panel |

---

## Dos and Don'ts

| Do | Don't |
|----|-------|
| All caps | Mixed case text |
| Amber on black | Bright white text |
| Chunky segmented bars | Smooth gradient fills |
| Hard corners | Rounded corners |
| Box-drawing borders | Drop shadows |
| Blinking indicators | Animations / transitions |
| Monospace only | Proportional fonts |
| Minimal elements | Decorative imagery or icons |
