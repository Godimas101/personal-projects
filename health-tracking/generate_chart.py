#!/usr/bin/env python3
"""
github-graphs — Markdown Table → SVG Chart Generator
Reads any markdown table and charts one or two numeric columns over time.

Config via environment variables:
  MONTHS        Rolling window in months (default: 6)
  INPUT_FILE    Path to the markdown file containing the table
  OUTPUT_FILE   Path to write the SVG output

  DATE_COL      Column index (0-based) or exact header name for the date column (default: 0)
  Y1_COL        Column index or header name for the primary (left) y-axis (default: 1)
  Y2_COL        Column index or header name for the secondary (right) y-axis (optional)

  Y1_LABEL      Left axis label  (default: the column header name)
  Y2_LABEL      Right axis label (default: the column header name)
  TITLE         Chart title      (default: auto-generated from column names)
  STRIP_CHARS   Characters to remove from values before parsing, e.g. "%" (default: "%")
  SHOW_TREND    Whether to draw a linear trendline on Y1 — "true" or "false" (default: true)
"""

import os
import re
import sys
from datetime import datetime
from dateutil.relativedelta import relativedelta

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

# ── Config ────────────────────────────────────────────────────────────────────

MONTHS      = int(os.environ.get("MONTHS",     "6"))
INPUT_FILE  =     os.environ.get("INPUT_FILE",  "health-tracking/weight-tracking.md")
OUTPUT_FILE =     os.environ.get("OUTPUT_FILE", "health-tracking/charts/weight-chart.svg")

DATE_COL    =     os.environ.get("DATE_COL",   "0")
Y1_COL      =     os.environ.get("Y1_COL",     "1")
Y2_COL      =     os.environ.get("Y2_COL",     "").strip()

Y1_LABEL    =     os.environ.get("Y1_LABEL",   "").strip()
Y2_LABEL    =     os.environ.get("Y2_LABEL",   "").strip()
TITLE       =     os.environ.get("TITLE",      "").strip()
STRIP_CHARS =     os.environ.get("STRIP_CHARS", "%")
SHOW_TREND  =     os.environ.get("SHOW_TREND", "true").strip().lower() == "true"

# ── GitHub dark theme palette ─────────────────────────────────────────────────

BG         = "#0d1117"
SURFACE    = "#161b22"
BORDER     = "#30363d"
TEXT       = "#e6edf3"
TEXT_MUTED = "#8b949e"
BLUE       = "#58a6ff"
ORANGE     = "#f97316"
TREND_COL  = "#388bfd"

# ── Markdown table parser ─────────────────────────────────────────────────────

TABLE_ROW_RE  = re.compile(r"^\|(.+)\|$")
SEPARATOR_RE  = re.compile(r"^\|[\s|:-]+\|$")
DATE_FORMATS  = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]


def find_table(content):
    """Return (headers, data_rows) from the first valid markdown table found."""
    lines = content.splitlines()
    i = 0
    while i < len(lines):
        # Look for a header row
        m = TABLE_ROW_RE.match(lines[i].strip())
        if m and i + 1 < len(lines) and SEPARATOR_RE.match(lines[i + 1].strip()):
            headers = [c.strip() for c in lines[i].split("|")[1:-1]]
            data_rows = []
            j = i + 2
            while j < len(lines):
                row_m = TABLE_ROW_RE.match(lines[j].strip())
                if not row_m:
                    break
                cells = [c.strip() for c in lines[j].split("|")[1:-1]]
                # Pad if the row is shorter than the header (trailing empty cols)
                while len(cells) < len(headers):
                    cells.append("")
                data_rows.append(cells)
                j += 1
            if data_rows:
                return headers, data_rows
        i += 1
    return None, None


def resolve_col(headers, spec):
    """Return the integer index for a column spec (int string or header name)."""
    try:
        idx = int(spec)
        if 0 <= idx < len(headers):
            return idx
        raise ValueError(f"Column index {idx} out of range (table has {len(headers)} columns).")
    except ValueError:
        pass
    lower = spec.lower()
    for i, h in enumerate(headers):
        if h.lower() == lower:
            return i
    raise ValueError(f"Column '{spec}' not found. Available headers: {headers}")


def parse_date(raw):
    s = raw.strip().rstrip("Z")
    # Try with just the first part if there's extra tokens
    for fmt in DATE_FORMATS:
        for candidate in [s, s.split()[0]]:
            try:
                return datetime.strptime(candidate, fmt)
            except ValueError:
                continue
    return None


def parse_value(raw):
    cleaned = raw.strip()
    for ch in STRIP_CHARS:
        cleaned = cleaned.replace(ch, "")
    cleaned = cleaned.strip()
    if not cleaned:
        return None
    try:
        return float(cleaned)
    except ValueError:
        return None

# ── Data loading ──────────────────────────────────────────────────────────────

def load_data(path):
    with open(path, encoding="utf-8") as f:
        content = f.read()

    headers, rows = find_table(content)
    if headers is None:
        print("ERROR: No markdown table found in the file.")
        sys.exit(1)

    date_idx = resolve_col(headers, DATE_COL)
    y1_idx   = resolve_col(headers, Y1_COL)
    y2_idx   = resolve_col(headers, Y2_COL) if Y2_COL else None

    col_name_y1 = headers[y1_idx]
    col_name_y2 = headers[y2_idx] if y2_idx is not None else None

    cutoff = datetime.now() - relativedelta(months=MONTHS)

    dates, y1_vals, y2_vals = [], [], []

    for cells in rows:
        date = parse_date(cells[date_idx])
        if date is None or date < cutoff:
            continue

        v1 = parse_value(cells[y1_idx])
        if v1 is None:
            continue  # skip rows with no primary value

        v2 = parse_value(cells[y2_idx]) if y2_idx is not None else None

        dates.append(date)
        y1_vals.append(v1)
        y2_vals.append(v2)

    return dates, y1_vals, y2_vals, col_name_y1, col_name_y2

# ── Chart generation ──────────────────────────────────────────────────────────

def generate_chart(dates, y1_vals, y2_vals, col_name_y1, col_name_y2, output_path):
    label_y1 = Y1_LABEL or col_name_y1
    label_y2 = Y2_LABEL or col_name_y2 or ""
    title    = TITLE or f"{col_name_y1} — Last {MONTHS} Months"

    fig, ax1 = plt.subplots(figsize=(13, 5))
    fig.patch.set_facecolor(BG)
    ax1.set_facecolor(BG)

    # ── Primary line ──────────────────────────────────────────────────────────
    ax1.plot(dates, y1_vals,
             color=BLUE, linewidth=2, marker="o", markersize=4,
             label=label_y1, zorder=3)

    # ── Trendline ─────────────────────────────────────────────────────────────
    if SHOW_TREND and len(dates) >= 2:
        x_num = mdates.date2num(dates)
        z = np.polyfit(x_num, y1_vals, 1)
        p = np.poly1d(z)
        trend_x = [min(dates), max(dates)]
        ax1.plot(trend_x, p(mdates.date2num(trend_x)),
                 linestyle="--", color=TREND_COL, linewidth=1.5, alpha=0.75,
                 label=f"{label_y1} trend", zorder=2)

    # ── Secondary axis ────────────────────────────────────────────────────────
    valid = [(d, v) for d, v in zip(dates, y2_vals) if v is not None]
    lines2, labels2 = [], []

    if valid and col_name_y2:
        vdates, vvals = zip(*valid)
        ax2 = ax1.twinx()
        ax2.set_facecolor(BG)
        ax2.plot(vdates, vvals,
                 color=ORANGE, linewidth=1.5, marker="s", markersize=3,
                 alpha=0.85, label=label_y2)
        ax2.set_ylabel(label_y2, color=ORANGE, fontsize=10)
        ax2.tick_params(axis="y", colors=ORANGE, labelsize=9)
        for spine in ax2.spines.values():
            spine.set_color(BORDER)
        lines2, labels2 = ax2.get_legend_handles_labels()

    # ── Left axis styling ─────────────────────────────────────────────────────
    ax1.set_ylabel(label_y1, color=BLUE, fontsize=10)
    ax1.tick_params(axis="y", colors=BLUE, labelsize=9)
    ax1.tick_params(axis="x", colors=TEXT_MUTED, labelsize=9, rotation=45)
    ax1.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    for spine in ax1.spines.values():
        spine.set_color(BORDER)
    ax1.grid(True, color=BORDER, linestyle="-", linewidth=0.5)

    # ── Title and legend ──────────────────────────────────────────────────────
    ax1.set_title(title, color=TEXT, fontsize=13, pad=12, fontweight="bold")

    lines1, labels1 = ax1.get_legend_handles_labels()
    ax1.legend(
        lines1 + lines2, labels1 + labels2,
        facecolor=SURFACE, edgecolor=BORDER, labelcolor=TEXT,
        fontsize=9, loc="upper right",
    )

    plt.tight_layout()

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    plt.savefig(output_path, format="svg", facecolor=BG, bbox_inches="tight")
    plt.close()
    print(f"✓ Chart written to {output_path}")

# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    dates, y1_vals, y2_vals, col_name_y1, col_name_y2 = load_data(INPUT_FILE)

    if not dates:
        print(f"No data found in the last {MONTHS} months. Nothing to chart.")
        sys.exit(0)

    print(f"Charting {len(dates)} entries over the last {MONTHS} months.")
    generate_chart(dates, y1_vals, y2_vals, col_name_y1, col_name_y2, OUTPUT_FILE)
