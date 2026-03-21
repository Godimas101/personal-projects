# Claude Usage Monitor — Style Guide

> Hybrid aesthetic: NASA Punk structure + Cassette Futurism warmth.
> Amber phosphor terminals. Functional, industrial, utilitarian.
> Inspired by Weyland-Yutani terminals, NASA control rooms, and early CRT computing.

---

## Aesthetic Research Summary

### What NASA Punk actually is
NASA Punk is grounded in **real spacecraft and control room design** from the 1960s–70s space race. Key principle: everything visibly serves a purpose. No ornament. Modular, practical, lived-in. The Aliens franchise draws directly from this — the GRiD Compass computers used on film were real military hardware. The Weyland-Yutani terminals are simple monochrome displays using fonts like **Eurostile / Microgramma Bold Extended** — not elaborate fantasy UI.

**Critical insight from research:** Real NASA control rooms and military terminals use *simple, basic graphics*. The more sophisticated the operation, the simpler the display. Our widget should feel like a real instrument readout, not a movie prop.

### What Cassette Futurism actually is
Cassette Futurism spans the **early 1970s to mid-1990s** — the analog-to-digital transition era. What distinguishes it from generic "80s design":
- Emphasises visible, physical interaction (mechanical buttons, tactile feedback)
- Celebrates raw early microprocessor hardware: CRT monitors, floppy disks, VU meters
- Low-resolution grids (8×8 or 16×16 pixels) reflecting actual hardware constraints
- Two colour directions: **neon/cyberpunk** (purples, magentas) OR **warm analog glow** (amber, green CRT)

We're using the **warm analog glow** direction — amber phosphor CRT, not neon synthwave.

### Our hybrid approach
- **NASA Punk structure**: symmetrical grid layout, functional grouping, graphical status at-a-glance
- **Cassette Futurism warmth**: amber phosphor, scanlines, chunky segmented bars, beveled elements
- **Weyland-Yutani typography**: Eurostile/Microgramma (all-caps, industrial authority)
- Result: looks like a real instrument panel from a 1980s spacecraft

---

## Colour Palette

| Token | Hex | Role |
|-------|-----|------|
| `BG` | `#090909` | Window background — CRT black |
| `PANEL` | `#0f0e0c` | Panel backgrounds — barely warm black |
| `BORDER_DIM` | `#2a1f0a` | Inactive panel borders |
| `BORDER` | `#4a3510` | Active panel borders |
| `AMBER` | `#e8a020` | Primary text — classic amber phosphor |
| `AMBER_BRIGHT` | `#ffb300` | Key values, percentages — bright phosphor |
| `AMBER_DIM` | `#7a5010` | Secondary labels, metadata |
| `AMBER_GLOW` | `#ff9900` | Active indicator, blinking cursor |
| `GREEN` | `#00cc44` | Good state — usage low |
| `YELLOW` | `#ffbf00` | Warning state — usage moderate |
| `RED` | `#cc2200` | Alert state — usage high / rate limited |
| `BEVEL_LIGHT` | `#5a4020` | Top/left bevel edge (lighter) |
| `BEVEL_DARK` | `#1a0e04` | Bottom/right bevel edge (darker) |
| `SCANLINE` | `#0d0c0a` | Scanline stripes |

```python
BG           = "#090909"
PANEL        = "#0f0e0c"
BORDER_DIM   = "#2a1f0a"
BORDER       = "#4a3510"
AMBER        = "#e8a020"
AMBER_BRIGHT = "#ffb300"
AMBER_DIM    = "#7a5010"
AMBER_GLOW   = "#ff9900"
GREEN        = "#00cc44"
YELLOW       = "#ffbf00"
RED          = "#cc2200"
BEVEL_LIGHT  = "#5a4020"
BEVEL_DARK   = "#1a0e04"
SCANLINE     = "#0d0c0a"
```

### Usage → colour mapping
```python
def usage_colour(pct: float) -> str:
    if pct < 0.60:  return GREEN
    if pct < 0.85:  return YELLOW
    return RED
```

---

## Typography

### Preferred fonts (in order)
1. **Eurostile** or **Microgramma Bold Extended** — the actual Weyland-Yutani font. All-caps, wide, industrial. If installed.
2. **Nasalization** — derived from NASA's 1975 worm logo. 6-weight family. Free via Adobe Fonts.
3. **Astro Punk** — designed specifically for 1960s space race console aesthetic. Monospace.
4. **Courier New** — reliable fallback. Monospace, period-appropriate.
5. **Consolas** — cleaner monospace fallback.

**Rules:**
- All text displayed in UPPERCASE
- No proportional fonts — monospace only
- Tight to moderate letter spacing (functional, no flourish)

```python
FONT_PREFERRED = ["Eurostile", "Microgramma", "Nasalization", "Courier New", "Consolas"]

def best_font(size: int, bold: bool = False) -> tuple:
    """Return the first available preferred font."""
    import tkinter.font as tkfont
    available = tkfont.families()
    for name in FONT_PREFERRED:
        if name in available:
            weight = "bold" if bold else "normal"
            return (name, size, weight)
    weight = "bold" if bold else "normal"
    return ("Courier New", size, weight)
```

### Font scale
| Token | Spec | Usage |
|-------|------|-------|
| `FONT_TINY` | size 7 | Metadata, scanline labels |
| `FONT_SMALL` | size 8 | Secondary labels |
| `FONT_BODY` | size 9 | Standard panel text |
| `FONT_VALUE` | size 11 bold | Key numbers, percentages |
| `FONT_TITLE` | size 9 bold | Panel headers, section labels |

---

## UI Elements

### Progress Bar (segmented)

Discrete blocks — never a smooth fill. Reflects actual CRT hardware limitations.

**Character version (for fallback):**
```python
FILLED = "▓"
EMPTY  = "░"

def render_bar(pct: float, segments: int = 16) -> str:
    n = round(pct * segments)
    return FILLED * n + EMPTY * (segments - n)
# → "▓▓▓▓▓▓░░░░░░░░░░"
```

**Canvas version (preferred):**
Draw filled rectangles with 1px gaps. Each segment = `(bar_width - gaps) / segments` px wide.
Colour changes based on `usage_colour(pct)`.

### Beveled panel border (Cassette Futurism depth)

Two-line border creates a faux 3D inset. Outer = `BEVEL_DARK`, inner = `BEVEL_LIGHT`. Reversed for a raised look.

```python
# Inset/recessed panel:
canvas.create_rectangle(x, y, x+w, y+h, outline=BEVEL_DARK,  width=1)  # outer
canvas.create_rectangle(x+1, y+1, x+w-1, y+h-1, outline=BEVEL_LIGHT, width=1)  # inner
```

### Status indicator light

Small filled circle. Changes colour by state. No border.

```python
# States:
canvas.create_oval(x, y, x+6, y+6, fill=GREEN,     outline="")  # nominal
canvas.create_oval(x, y, x+6, y+6, fill=YELLOW,    outline="")  # warning
canvas.create_oval(x, y, x+6, y+6, fill=RED,        outline="")  # alert
canvas.create_oval(x, y, x+6, y+6, fill=AMBER_DIM,  outline="")  # inactive
```

### Blinking cursor / alive indicator

One element blinks at 900ms to signal the system is live. A small `▮` or filled rect.

```python
def _blink(self):
    self._cursor_on = not self._cursor_on
    fill = AMBER_GLOW if self._cursor_on else BG
    self._canvas.itemconfig(self._cursor_id, fill=fill)
    self._root.after(900, self._blink)
```

### Scanline overlay

Horizontal lines at every 2px, drawn LAST so they overlay everything.

```python
for y in range(0, canvas_height, 2):
    canvas.create_line(0, y, canvas_width, y,
                       fill=SCANLINE, stipple="gray50")
```

Use on the widget background only — not the options panel.

---

## Widget Layout

```
╔══════════════════════════════╗
║ ● CLAUDE           [⚙]      ║  ← indicator + title + settings btn
╠══════════════════════════════╣
║ SESSION                      ║
║ ▓▓▓▓▓▓░░░░░░░░░░  38%  4H12M║  ← bar + pct + reset timer
╠══════════════════════════════╣
║ WEEKLY                       ║
║ ▓▓▓░░░░░░░░░░░░░  13%  6D01H║
╚══════════════════════════════╝
```

- Width: ~250px
- Height: ~95px
- `overrideredirect(True)` — no window chrome
- `wm_attributes("-topmost", True)` — always on top
- `WS_EX_TOOLWINDOW` via ctypes — no taskbar button
- Draggable via mouse drag anywhere on the widget
- Right-click or ⚙ button opens options panel
- Scanlines drawn over entire background

---

## Options Panel Layout

Standard Toplevel with chrome (this window gets a title bar).

**Tab structure:**

```
┌─────────────────────────────────┐
│  CLAUDE USAGE MONITOR  v0.1.0   │
├──────────┬──────────────────────┤
│ GENERAL  │  STATS               │
├──────────┴──────────────────────┤
│  (tab content)                  │
└─────────────────────────────────┘
```

**General tab layout:**
```
╔══════════════════════════════════╗
║ SETTINGS                         ║
╠══════════════════════════════════╣
║ POLL INTERVAL     [15 MIN  ▼]    ║
║ LAUNCH ON STARTUP [■ ENABLED]    ║
╠══════════════════════════════════╣
║ ABOUT                            ║
╠══════════════════════════════════╣
║ VERSION           0.1.0          ║
║ AUTHORS           CHRIS CARPENTER║
║                   CLAUDE S4.6    ║
║ REPOSITORY        [LINK]         ║
╚══════════════════════════════════╝
```

**Stats tab layout:**
```
╔══════════════════════════════════╗
║ RATE LIMITS                      ║
╠══════════════════════════════════╣
║ 5-HOUR    ▓▓▓▓▓░░░░░  38%  4H12M║
║ 7-DAY     ▓▓░░░░░░░░  13%  6D1H ║
║ OPUS-7D   ▓░░░░░░░░░   9%  6D1H ║
╠══════════════════════════════════╣
║ TODAY                            ║
╠══════════════════════════════════╣
║ MESSAGES          142            ║
║ OUTPUT TOKENS     48.2K          ║
║ INPUT TOKENS      12.1K          ║
║ CACHE READ        8.3K           ║
╠══════════════════════════════════╣
║ BURN RATE   1,240 TOK/MIN  FAST  ║
╠══════════════════════════════════╣
║ ALL TIME                         ║
╠══════════════════════════════════╣
║ MESSAGES          3,860          ║
║ OUTPUT TOKENS     1.2M           ║
║ SESSIONS          9              ║
║ DAYS ACTIVE       9              ║
╚══════════════════════════════════╝
```

---

## Window Behaviour

| Property | Value |
|----------|-------|
| Widget background | `BG` |
| Always on top | Yes |
| Taskbar button | No (`WS_EX_TOOLWINDOW`) |
| Focus steal | No (`WS_EX_NOACTIVATE`) |
| Draggable | Yes — anywhere on widget |
| Right-click | Opens options panel |

---

## Dos and Don'ts

| Do | Don't |
|----|-------|
| All uppercase text | Mixed or lowercase text |
| Amber on near-black | Bright white or pure black text |
| Chunky segmented bars | Smooth gradient fills |
| Hard corners | Rounded corners |
| Beveled borders (inset/raised) | Drop shadows |
| One blinking element | Animations, transitions, easing |
| Monospace only | Proportional fonts |
| Functional layout only | Decorative imagery or icons |
| Scanlines on widget bg | Scanlines on the options panel |
| Red/amber/green for state | Other colours for state |

---

## Design References

- [NASA Graphics Standards Manual (1975)](https://www.nasa.gov/wp-content/uploads/2015/01/nasa_graphics_manual_nhb_1430-2_jan_1976.pdf)
- [Fonts In Use — Weyland-Yutani](https://fontsinuse.com/uses/35613/weyland-yutani-corp-logo-and-slogan-in-aliens)
- [Cassette Futurism — Aesthetics Wiki](https://aesthetics.fandom.com/wiki/Cassette_Futurism)
- [Typeset In The Future — Eurostile](https://typesetinthefuture.com/2014/11/29/fontspots-eurostile/)
- [HUDS+GUIS — Alien Romulus UI](https://www.hudsandguis.com/home/2025/alien-romulus)
- [Nasalization Font](https://fonts.adobe.com/fonts/nasalization)
- [Astro Punk Font](https://fontbundles.net/parker-creative/3232465-astro-punk-nasa-punk-monospace-font)
