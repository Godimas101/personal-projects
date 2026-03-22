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

THEMES = {
    "Default": dict(
        BG="#090909", PANEL="#0f0e0c", BORDER_DIM="#2a1f0a", BORDER="#4a3510",
        AMBER="#e8a020", AMBER_BRIGHT="#ffb300", AMBER_DIM="#7a5010", AMBER_GLOW="#ff9900",
        BEVEL_LIGHT="#5a4020", BEVEL_DARK="#1a0e04", SCANLINE="#0d0c0a",
        GREEN="#00cc44", YELLOW="#ffbf00", RED="#cc2200",
    ),
    "Red": dict(
        BG="#090909", PANEL="#0f0d0d", BORDER_DIM="#2a0c0a", BORDER="#4a1410",
        AMBER="#e83018", AMBER_BRIGHT="#ff3311", AMBER_DIM="#7a1808", AMBER_GLOW="#ff2200",
        BEVEL_LIGHT="#5a2018", BEVEL_DARK="#1a0804", SCANLINE="#0d0a0a",
        GREEN="#00cc44", YELLOW="#ffbf00", RED="#ff2200",
    ),
    "Blue": dict(
        BG="#090909", PANEL="#0d0d10", BORDER_DIM="#0a1028", BORDER="#10184a",
        AMBER="#2070e0", AMBER_BRIGHT="#3388ff", AMBER_DIM="#101870", AMBER_GLOW="#0066ff",
        BEVEL_LIGHT="#103858", BEVEL_DARK="#04041a", SCANLINE="#0a0a0d",
        GREEN="#00cc44", YELLOW="#ffbf00", RED="#cc2200",
    ),
    "Green": dict(
        BG="#090909", PANEL="#0c0f0c", BORDER_DIM="#082008", BORDER="#0c4010",
        AMBER="#20c840", AMBER_BRIGHT="#33ff55", AMBER_DIM="#086018", AMBER_GLOW="#00ee33",
        BEVEL_LIGHT="#185828", BEVEL_DARK="#041204", SCANLINE="#0a0d0a",
        GREEN="#33ff55", YELLOW="#ffbf00", RED="#cc2200",
    ),
    "Purple": dict(
        BG="#090909", PANEL="#0e0d10", BORDER_DIM="#180a28", BORDER="#28104a",
        AMBER="#b040d8", AMBER_BRIGHT="#cc55ff", AMBER_DIM="#581068", AMBER_GLOW="#aa00ff",
        BEVEL_LIGHT="#481858", BEVEL_DARK="#10041a", SCANLINE="#0b0a0d",
        GREEN="#00cc44", YELLOW="#ffbf00", RED="#cc2200",
    ),
    "Cyan": dict(
        BG="#090909", PANEL="#0c0f10", BORDER_DIM="#082020", BORDER="#0c4040",
        AMBER="#18c8cc", AMBER_BRIGHT="#22e8f0", AMBER_DIM="#086068", AMBER_GLOW="#00e0f0",
        BEVEL_LIGHT="#105858", BEVEL_DARK="#041414", SCANLINE="#0a0c0d",
        GREEN="#00cc44", YELLOW="#ffbf00", RED="#cc2200",
    ),
    "Orange": dict(
        BG="#090909", PANEL="#0f0e0b", BORDER_DIM="#2a1808", BORDER="#4a2808",
        AMBER="#f06010", AMBER_BRIGHT="#ff7700", AMBER_DIM="#803010", AMBER_GLOW="#ff5500",
        BEVEL_LIGHT="#603020", BEVEL_DARK="#1a0804", SCANLINE="#0d0b0a",
        GREEN="#00cc44", YELLOW="#ffbf00", RED="#cc2200",
    ),
    "White": dict(
        BG="#090909", PANEL="#0e0e0e", BORDER_DIM="#282828", BORDER="#484848",
        AMBER="#c8c8c8", AMBER_BRIGHT="#f0f0f0", AMBER_DIM="#606060", AMBER_GLOW="#ffffff",
        BEVEL_LIGHT="#484848", BEVEL_DARK="#141414", SCANLINE="#0c0c0c",
        GREEN="#00cc44", YELLOW="#ffbf00", RED="#cc2200",
    ),
}

THEME_NAMES = list(THEMES.keys())


def apply_theme(name: str) -> None:
    """Apply a named theme palette to this module's colour globals."""
    import sys
    m = sys.modules[__name__]
    for k, v in THEMES.get(name, THEMES["Default"]).items():
        setattr(m, k, v)

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

def bar_actual_width(w: int, segments: int = 14) -> int:
    """Actual pixel span of all pips in a draw_bar call (may be less than w)."""
    gap   = 1
    seg_w = max(2, (w - (segments - 1) * gap) // segments)
    return segments * (seg_w + gap) - gap


def bar_pip_edge(x: int, w: int, pct: float, segments: int = 14) -> int:
    """Return x pixel of the right edge of the last filled pip (matches draw_bar math)."""
    pct    = max(0.0, min(1.0, pct))
    filled = round(pct * segments)
    if filled == 0:
        return x
    gap   = 1
    seg_w = max(2, (w - (segments - 1) * gap) // segments)
    return x + filled * (seg_w + gap) - gap


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
