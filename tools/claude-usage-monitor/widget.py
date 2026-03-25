# widget.py — FloatingWidget and TaskbarWidget

import threading
import tkinter as tk

import theme as T
import usage_reader
import win_utils

# ── Floating layout constants ──────────────────────────────────────────────────
W        = 224
H        = 92
PAD      = 8
HEADER_H = 22
SEP_Y1   = HEADER_H
SEP_Y2   = HEADER_H + 1 + 33
BAR_H    = 11
RIGHT_W  = 32
BAR_W    = W - 2 * PAD - RIGHT_W

# ── Taskbar layout constants ───────────────────────────────────────────────────
W_EMBED    = 260
VSEP_1     = 66
VSEP_2     = 163
BAR_W_E    = 48
BAR_SEGS_E = 10


# ── Shared polling mixin ───────────────────────────────────────────────────────

class _PollMixin:
    """Provides fetch/poll loop and data storage. Subclass must set self._win and self._settings."""

    def _poll_init(self):
        self._poll()

    def _poll(self):
        if win_utils.should_pause():
            self._paused = True
            self._redraw()
            self._win.after(10_000, self._poll)
            return
        self._paused = False
        threading.Thread(target=self._fetch, daemon=True).start()

    def _fetch(self):
        rate  = usage_reader.fetch_rate_limits()
        local = usage_reader.scan_local()
        self._win.after(0, lambda: self._on_data(rate, local))

    def _on_data(self, rate, local):
        # Only overwrite with new data — never replace good data with None
        if rate is not None:
            self._rate_data = rate
        if local is not None:
            self._local = local
        self._redraw()
        if cb := self._settings.get("_on_data_cb"):
            try:
                cb(self._rate_data, self._local)
            except Exception:
                pass
        interval = self._settings.get("poll_interval_ms", 15 * 60 * 1000)
        self._win.after(interval, self._poll)

    def _open_options(self):
        import options
        options.open_panel(
            self._win, self._settings,
            self._rate_data, self._local,
            on_settings_change=None,
        )


# ══════════════════════════════════════════════════════════════════════════════
# Floating Widget
# ══════════════════════════════════════════════════════════════════════════════

class FloatingWidget(_PollMixin):

    def __init__(self, root: tk.Tk, settings: dict):
        self._settings   = settings
        self._cursor_on  = True
        self._drag_ox    = 0
        self._drag_oy    = 0
        self._rate_data  = None
        self._local      = None
        self._paused     = False

        self._win = tk.Toplevel(root)
        self._win.overrideredirect(True)
        self._win.attributes("-toolwindow", True)
        self._win.attributes("-topmost", True)
        self._win.configure(bg=T.BG)
        self._win.geometry(f"{W}x{H}")
        self._win.resizable(False, False)

        self._canvas = tk.Canvas(self._win, width=W, height=H,
                                  bg=T.BG, highlightthickness=0)
        self._canvas.pack()
        self._canvas.bind("<ButtonPress-1>",  self._on_press)
        self._canvas.bind("<B1-Motion>",       self._on_drag)
        self._canvas.bind("<ButtonRelease-1>", self._on_release)
        self._canvas.bind("<Button-3>",        lambda e: self._open_options())
        self._canvas.bind("<Double-Button-1>", lambda e: self._open_options())

        self._apply_win32()
        self._position()
        self._blink()
        self._poll_init()

    def _apply_win32(self):
        try:
            self._win.update_idletasks()
            win_utils.set_tool_window(self._win.winfo_id())
        except Exception:
            pass

    def _position(self):
        saved = self._settings.get("position")
        if saved:
            self._win.geometry(f"{W}x{H}+{saved['x']}+{saved['y']}")
            return
        try:
            rect = win_utils.get_tray_rect()
            x = rect.right - W - 4
            y = rect.top   - H - 4
            self._win.geometry(f"{W}x{H}+{x}+{y}")
        except Exception:
            sw = self._win.winfo_screenwidth()
            sh = self._win.winfo_screenheight()
            self._win.geometry(f"{W}x{H}+{sw - W - 8}+{sh - H - 48}")

    def _blink(self):
        self._cursor_on = not self._cursor_on
        self._redraw()
        self._win.after(900, self._blink)

    def _redraw(self):
        c = self._canvas
        c.delete("all")

        transparent = self._settings.get("float_transparent_bg", False)
        text_fx     = self._settings.get("float_text_fx", True) and not transparent
        self._win.attributes("-transparentcolor", T.BG if transparent else "")

        rate  = self._rate_data
        loading     = rate is None
        five_h_pct  = rate.five_hour_pct  / 100 if rate else 0.0
        seven_d_pct = rate.seven_day_pct  / 100 if rate else 0.0
        five_h_cd   = rate.five_hour_countdown  if rate else "..."
        seven_d_cd  = rate.seven_day_countdown  if rate else "..."

        f_title = T.best_font(9, bold=True)
        f_value = T.best_font(9, bold=True)

        c.create_rectangle(0, 0, W, H, fill=T.BG, outline="")
        if text_fx:
            T.draw_bevel(c, 0, 0, W - 1, H - 1)

        # Header
        dot_fill = T.AMBER_GLOW if self._cursor_on else T.AMBER_DIM
        c.create_oval(PAD, HEADER_H // 2 - 4, PAD + 8, HEADER_H // 2 + 4,
                      fill=dot_fill, outline="")
        c.create_text(PAD + 14, HEADER_H // 2, text="CLAUDE", anchor="w",
                      fill=T.AMBER_BRIGHT, font=f_title)
        status_text  = "PAUSED" if self._paused else "LIVE"
        status_color = T.AMBER_DIM if self._paused else T.GREEN
        c.create_text(W - PAD - 28, HEADER_H // 2, text=status_text, anchor="w",
                      fill=status_color, font=f_title)
        c.create_line(0, SEP_Y1, W, SEP_Y1, fill=T.BORDER_DIM)

        five_h_tf  = rate.five_hour_time_frac  if rate else 0.0
        seven_d_tf = rate.seven_day_time_frac  if rate else 0.0

        actual_bar_w = T.bar_actual_width(BAR_W)

        def draw_time_line(bx, by, elapsed_frac):
            """Horizontal filling line above a bar. Green=elapsed, dull=remaining."""
            ly = by - 4
            c.create_rectangle(bx, ly, bx + actual_bar_w, ly + 2, fill=T.AMBER_DIM, outline="")
            rw = int(actual_bar_w * elapsed_frac)
            if rw > 0:
                c.create_rectangle(bx, ly, bx + rw, ly + 2, fill=T.GREEN, outline="")

        def draw_usage_cursor(bx, by, bh, usage_frac):
            """Vertical line anchored to right edge of the highest filled pip."""
            cx = T.bar_pip_edge(bx, BAR_W, usage_frac)
            c.create_line(cx, by - 2, cx, by + bh + 2, fill=T.GREEN, width=2)

        # SESSION bar
        y0 = SEP_Y1 + 1
        c.create_text(PAD, y0 + 5, text="SESSION", anchor="w",
                      fill=T.AMBER_DIM, font=T.best_font(7))
        bar_y = y0 + 17
        T.draw_bar(c, PAD, bar_y, BAR_W, BAR_H, five_h_pct)
        if not loading:
            draw_time_line(PAD, bar_y, five_h_tf)
            draw_usage_cursor(PAD, bar_y, BAR_H, five_h_pct)
        rx = PAD + BAR_W + 4
        c.create_text(rx, bar_y + (BAR_H // 2), anchor="w",
                      text="..." if loading else f"{T.fmt_pct(five_h_pct):>4}",
                      fill=T.AMBER_DIM if loading else T.usage_colour(five_h_pct), font=f_value)
        c.create_line(0, SEP_Y2, W, SEP_Y2, fill=T.BORDER_DIM)

        # WEEKLY bar
        y1 = SEP_Y2 + 1
        c.create_text(PAD, y1 + 5, text="WEEKLY", anchor="w",
                      fill=T.AMBER_DIM, font=T.best_font(7))
        bar_y2 = y1 + 17
        T.draw_bar(c, PAD, bar_y2, BAR_W, BAR_H, seven_d_pct)
        if not loading:
            draw_time_line(PAD, bar_y2, seven_d_tf)
            draw_usage_cursor(PAD, bar_y2, BAR_H, seven_d_pct)
        c.create_text(rx, bar_y2 + (BAR_H // 2), anchor="w",
                      text="..." if loading else f"{T.fmt_pct(seven_d_pct):>4}",
                      fill=T.AMBER_DIM if loading else T.usage_colour(seven_d_pct), font=f_value)

        if text_fx:
            T.draw_scanlines(c, W, H)

    # ── Drag ──────────────────────────────────────────────────────────────────

    def _on_press(self, e):
        self._drag_ox = e.x_root - self._win.winfo_x()
        self._drag_oy = e.y_root - self._win.winfo_y()

    def _on_drag(self, e):
        self._win.geometry(f"+{e.x_root - self._drag_ox}+{e.y_root - self._drag_oy}")

    def _on_release(self, e):
        self._settings["position"] = {
            "x": self._win.winfo_x(),
            "y": self._win.winfo_y(),
        }

    # ── Lifecycle ─────────────────────────────────────────────────────────────

    def show(self):
        self._win.deiconify()

    def hide(self):
        self._win.withdraw()

    def destroy(self):
        self._win.destroy()


# ══════════════════════════════════════════════════════════════════════════════
# Taskbar Widget (embedded)
# ══════════════════════════════════════════════════════════════════════════════

class TaskbarWidget(_PollMixin):

    def __init__(self, root: tk.Tk, settings: dict):
        self._settings  = settings
        self._cursor_on = True
        self._embed_h   = 48
        self._embedded  = False
        self._rate_data = None
        self._local     = None
        self._paused    = False

        self._win = tk.Toplevel(root)
        self._win.overrideredirect(True)
        self._win.attributes("-toolwindow", True)
        self._win.attributes("-topmost", True)
        self._win.configure(bg=T.BG)
        self._win.resizable(False, False)

        self._canvas = tk.Canvas(self._win, width=W_EMBED, height=48,
                                  bg=T.BG, highlightthickness=0)
        self._canvas.pack()
        self._canvas.bind("<Button-3>",        lambda e: self._open_options())
        self._canvas.bind("<Double-Button-1>", lambda e: self._open_options())

        self._win.update_idletasks()
        self._apply_win32()
        self._reposition()
        self._reposition_loop()
        self._topmost_loop()
        self._blink()
        self._poll_init()

    def _apply_win32(self):
        try:
            self._win.update_idletasks()
            win_utils.set_tool_window(self._win.winfo_id())
        except Exception:
            pass

    def _reposition(self):
        """Snap to taskbar coordinates, bottom-anchored."""
        try:
            pos = win_utils.get_taskbar_position(W_EMBED)
            if pos:
                x, taskbar_top, taskbar_h = pos
                self._embed_h = max(taskbar_h - 1, 32)
                # Anchor to bottom so the thin line at taskbar top stays visible
                y = taskbar_top + taskbar_h - self._embed_h
                self._win.geometry(f"{W_EMBED}x{self._embed_h}+{x}+{y}")
                self._canvas.configure(height=self._embed_h)
        except Exception:
            pass

    def _reposition_loop(self):
        """Recheck taskbar position every 2s (handles taskbar moves/resize)."""
        self._reposition()
        self._win.after(2000, self._reposition_loop)

    def _topmost_loop(self):
        """Re-assert topmost every 300ms. Hide when a fullscreen app is running."""
        if win_utils.is_fullscreen():
            self._win.withdraw()
        else:
            if not self._win.winfo_viewable():
                self._win.deiconify()
            self._win.attributes("-topmost", True)
            self._win.lift()
        self._win.after(300, self._topmost_loop)

    def _blink(self):
        self._cursor_on = not self._cursor_on
        self._redraw()
        self._win.after(900, self._blink)

    def _redraw(self):
        c  = self._canvas
        c.delete("all")
        cw = W_EMBED
        ch = self._embed_h
        cy = ch // 2

        transparent = self._settings.get("taskbar_transparent_bg", False)
        text_fx     = self._settings.get("taskbar_text_fx", True) and not transparent
        self._win.attributes("-transparentcolor", T.BG if transparent else "")

        rate = self._rate_data
        five_h_pct  = rate.five_hour_pct      / 100 if rate else 0.0
        seven_d_pct = rate.seven_day_pct      / 100 if rate else 0.0
        five_h_tf   = rate.five_hour_time_frac      if rate else 0.0
        seven_d_tf  = rate.seven_day_time_frac      if rate else 0.0

        f7  = T.best_font(7)
        f7b = T.best_font(7, bold=True)
        f8b = T.best_font(8, bold=True)

        c.create_rectangle(0, 0, cw, ch, fill=T.BG, outline="")

        dot_fill = T.AMBER_GLOW if self._cursor_on else T.AMBER_DIM
        c.create_oval(5, cy - 4, 13, cy + 4, fill=dot_fill, outline="")
        c.create_text(17, cy, text="CLAUDE", anchor="w",
                      fill=T.AMBER_BRIGHT, font=f8b)

        for vx in (VSEP_1, VSEP_2):
            c.create_line(vx, 4, vx, ch - 4, fill=T.BORDER_DIM)

        bar_top = cy - 4
        bar_h_e = 8

        actual_bar_w_e = T.bar_actual_width(BAR_W_E, BAR_SEGS_E)

        def draw_time_line_e(bx, elapsed_frac):
            ly = bar_top - 3
            c.create_rectangle(bx, ly, bx + actual_bar_w_e, ly + 2, fill=T.AMBER_DIM, outline="")
            rw = int(actual_bar_w_e * elapsed_frac)
            if rw > 0:
                c.create_rectangle(bx, ly, bx + rw, ly + 2, fill=T.GREEN, outline="")

        # 5H bar
        sx  = VSEP_1 + 6
        b1x = sx + 18
        c.create_text(sx, cy, text="5H", anchor="w", fill=T.AMBER_DIM, font=f7)
        T.draw_bar(c, b1x, bar_top, BAR_W_E, bar_h_e, five_h_pct, BAR_SEGS_E)
        if rate:
            draw_time_line_e(b1x, five_h_tf)
            ux = T.bar_pip_edge(b1x, BAR_W_E, five_h_pct, BAR_SEGS_E)
            c.create_line(ux, bar_top - 2, ux, bar_top + bar_h_e + 2, fill=T.GREEN, width=2)
        c.create_text(b1x + BAR_W_E + 3, cy, anchor="w",
                      text=T.fmt_pct(five_h_pct),
                      fill=T.usage_colour(five_h_pct), font=f7b)

        # 7D bar
        wx  = VSEP_2 + 6
        b2x = wx + 18
        c.create_text(wx, cy, text="7D", anchor="w", fill=T.AMBER_DIM, font=f7)
        T.draw_bar(c, b2x, bar_top, BAR_W_E, bar_h_e, seven_d_pct, BAR_SEGS_E)
        if rate:
            draw_time_line_e(b2x, seven_d_tf)
            ux2 = T.bar_pip_edge(b2x, BAR_W_E, seven_d_pct, BAR_SEGS_E)
            c.create_line(ux2, bar_top - 2, ux2, bar_top + bar_h_e + 2, fill=T.GREEN, width=2)
        c.create_text(b2x + BAR_W_E + 3, cy, anchor="w",
                      text=T.fmt_pct(seven_d_pct),
                      fill=T.usage_colour(seven_d_pct), font=f7b)

        if text_fx:
            T.draw_scanlines(c, cw, ch)

    # ── Lifecycle ─────────────────────────────────────────────────────────────

    def destroy(self):
        self._win.destroy()
