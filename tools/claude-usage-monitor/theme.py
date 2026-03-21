# theme.py — Colour palette, fonts, and drawing helpers
# Weyland-Yutani amber phosphor aesthetic

import tkinter.font as tkfont

# ── Colours ───────────────────────────────────────────────────────────────────
BG           = "#090909"   # CRT black
PANEL        = "#0f0e0c"   # panel background
BORDER_DIM   = "#2a1f0a"   # inactive border
BORDER       = "#4a3510"   # active border
AMBER        = "#e8a020"   # primary text — phosphor amber
AMBER_BRIGHT = "#ffb300"   # key values / percentages
AMBER_DIM    = "#7a5010"   # secondary labels / metadata
AMBER_GLOW   = "#ff9900"   # blinking cursor / active indicator
BEVEL_LIGHT  = "#5a4020"   # top/left bevel edge
BEVEL_DARK   = "#1a0e04"   # bottom/right bevel edge
SCANLINE     = "#0d0c0a"   # scanline stripe
GREEN        = "#00cc44"   # usage OK
YELLOW       = "#ffbf00"   # usage warning
RED          = "#cc2200"   # usage alert

# ── Typography ────────────────────────────────────────────────────────────────
_PREFERRED = ["Eurostile", "Microgramma", "Nasalization", "Courier New", "Consolas"]

def best_font(size: int, bold: bool = False) -> tuple:
    """Return the first available preferred font as a tkinter font tuple."""
    try:
        available = tkfont.families()
        for name in _PREFERRED:
            if name in available:
                return (name, size, "bold" if bold else "normal")
    except Exception:
        pass
    return ("Courier New", size, "bold" if bold else "normal")

# Pre-built font specs (call best_font once tk root exists)
def fonts() -> dict:
    return {
        "tiny":  best_font(7),
        "small": best_font(8),
        "body":  best_font(9),
        "title": best_font(9,  bold=True),
        "value": best_font(11, bold=True),
    }

# ── Utility ───────────────────────────────────────────────────────────────────
def usage_colour(pct: float) -> str:
    """Map a 0.0–1.0 usage fraction to a status colour."""
    if pct < 0.60: return GREEN
    if pct < 0.85: return YELLOW
    return RED

def fmt_tokens(n: int) -> str:
    if n >= 1_000_000: return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:     return f"{n / 1_000:.1f}K"
    return str(n)

def fmt_pct(pct: float) -> str:
    return f"{int(pct * 100)}%"

def render_bar(pct: float, segments: int = 14) -> str:
    """Return a text-based segmented bar string."""
    n = round(max(0.0, min(1.0, pct)) * segments)
    return "▓" * n + "░" * (segments - n)

def draw_bar(canvas, x: int, y: int, w: int, h: int,
             pct: float, segments: int = 14) -> None:
    """Draw a segmented progress bar on a canvas."""
    pct = max(0.0, min(1.0, pct))
    filled  = round(pct * segments)
    colour  = usage_colour(pct)
    gap     = 1
    seg_w   = max(2, (w - (segments - 1) * gap) // segments)

    for i in range(segments):
        x0 = x + i * (seg_w + gap)
        x1 = x0 + seg_w
        fill = colour if i < filled else BORDER_DIM
        canvas.create_rectangle(x0, y, x1, y + h, fill=fill, outline="")

def draw_scanlines(canvas, width: int, height: int) -> None:
    """Overlay scanlines across the entire canvas."""
    for scan_y in range(0, height, 2):
        canvas.create_line(0, scan_y, width, scan_y,
                           fill=SCANLINE, stipple="gray50")

def draw_bevel(canvas, x: int, y: int, w: int, h: int) -> None:
    """Draw a two-line beveled border (inset appearance)."""
    canvas.create_rectangle(x,   y,   x+w,   y+h,   outline=BEVEL_DARK,  width=1)
    canvas.create_rectangle(x+1, y+1, x+w-1, y+h-1, outline=BEVEL_LIGHT, width=1)
