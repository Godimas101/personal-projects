# options.py — Settings and stats panel

import json
import threading
import urllib.request
import tkinter as tk
import winreg
import sys

import theme as T
import usage_reader

APP_NAME        = "ClaudeUsageMonitor"
REPO_URL        = "https://github.com/Godimas101/personal-projects/tree/main/tools/claude-usage-monitor"
PATREON_URL     = "https://patreon.com/Godimas101"
SUPPORTERS_URL  = ("https://raw.githubusercontent.com/Godimas101/"
                   "personal-projects/main/patreon/supporters.json")
VERSION         = "1.0.0"

POLL_OPTIONS = [
    ("1 MIN",  1 * 60 * 1000),
    ("5 MIN",  5 * 60 * 1000),
    ("15 MIN", 15 * 60 * 1000),
    ("30 MIN", 30 * 60 * 1000),
    ("1 HOUR", 60 * 60 * 1000),
]

_panel = None   # singleton reference


def open_panel(parent, settings, rate_data, local_stats, on_settings_change=None):
    global _panel
    if _panel and _panel.winfo_exists():
        _panel.lift()
        return
    _panel = OptionsPanel(parent, settings, rate_data, local_stats, on_settings_change)


class OptionsPanel(tk.Toplevel):

    def __init__(self, parent, settings, rate_data, local_stats, on_settings_change):
        super().__init__(parent)
        self._settings   = settings
        self._rate_data  = rate_data
        self._local      = local_stats
        self._on_change  = on_settings_change
        self._active_tab = tk.StringVar(value="GENERAL")

        self._build()
        self._center(parent)

    # ── Build shell ───────────────────────────────────────────────────────────

    def _build(self):
        self.title("CLAUDE USAGE MONITOR")
        self.configure(bg=T.BG)
        self.resizable(False, False)
        self.attributes("-topmost", True)
        try:
            import sys, os
            base = sys._MEIPASS if getattr(sys, "frozen", False) else os.path.dirname(os.path.abspath(__file__))
            self.iconbitmap(os.path.join(base, "usage_monitor.ico"))
        except Exception:
            pass

        # Title bar
        hdr = tk.Frame(self, bg=T.PANEL, height=32)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text=f"CLAUDE USAGE MONITOR  v{VERSION}",
                 bg=T.PANEL, fg=T.AMBER_BRIGHT,
                 font=T.best_font(9, bold=True)).pack(side="left", padx=10, pady=6)

        tk.Frame(self, bg=T.BORDER, height=1).pack(fill="x")

        # Tab row
        tab_row = tk.Frame(self, bg=T.BG)
        tab_row.pack(fill="x")
        for label in ("GENERAL", "NERDS ONLY", "SUPPORTERS"):
            b = tk.Button(tab_row, text=label,
                          font=T.best_font(8, bold=True),
                          bd=0, relief="flat", cursor="hand2",
                          padx=12, pady=6,
                          command=lambda l=label: self._switch_tab(l))
            b.pack(side="left")
            b.configure(bg=T.BG, fg=T.AMBER_DIM,
                        activebackground=T.PANEL, activeforeground=T.AMBER)
            setattr(self, f"_tab_btn_{label.replace(' ', '_')}", b)

        tk.Frame(self, bg=T.BORDER, height=1).pack(fill="x")

        # Content area
        self._content = tk.Frame(self, bg=T.BG)
        self._content.pack(fill="both", expand=True)

        self._tab_general    = self._build_general(self._content)
        self._tab_nerds      = self._build_nerds(self._content)
        self._tab_supporters = self._build_supporters(self._content)

        # Size window to fit Nerds Only tab, then switch to General
        self._switch_tab("NERDS ONLY")
        self.update_idletasks()
        w = max(self.winfo_reqwidth(),  440)
        h = max(self.winfo_reqheight(), 400)
        self.geometry(f"{w}x{h}")
        self._switch_tab("GENERAL")

    def _rebuild(self):
        """Tear down and rebuild the panel with the current theme colours."""
        for w in self.winfo_children():
            w.destroy()
        self._active_tab = tk.StringVar(value="GENERAL")
        self._build()

    def _switch_tab(self, label: str):
        self._active_tab.set(label)
        self._tab_general.pack_forget()
        self._tab_nerds.pack_forget()
        self._tab_supporters.pack_forget()

        for tab_label in ("GENERAL", "NERDS ONLY", "SUPPORTERS"):
            btn = getattr(self, f"_tab_btn_{tab_label.replace(' ', '_')}")
            if tab_label == label:
                btn.configure(bg=T.PANEL, fg=T.AMBER_BRIGHT,
                              activebackground=T.PANEL, activeforeground=T.AMBER_BRIGHT)
            else:
                btn.configure(bg=T.BG, fg=T.AMBER_DIM,
                              activebackground=T.PANEL, activeforeground=T.AMBER)

        if label == "GENERAL":
            self._tab_general.pack(fill="both", expand=True)
        elif label == "NERDS ONLY":
            self._tab_nerds.pack(fill="both", expand=True)
        else:
            self._tab_supporters.pack(fill="both", expand=True)

    # ── General tab ───────────────────────────────────────────────────────────

    def _build_general(self, parent) -> tk.Frame:
        frame = tk.Frame(parent, bg=T.BG)

        def section(text):
            tk.Frame(frame, bg=T.BORDER, height=1).pack(fill="x", padx=10, pady=(10, 0))
            tk.Label(frame, text=text, bg=T.BG, fg=T.AMBER,
                     font=T.best_font(8, bold=True)).pack(anchor="w", padx=10, pady=(4, 2))

        def row(label, widget_cb):
            r = tk.Frame(frame, bg=T.BG)
            r.pack(fill="x", padx=10, pady=2)
            tk.Label(r, text=label, bg=T.BG, fg=T.AMBER_DIM,
                     font=T.best_font(8), width=18, anchor="w").pack(side="left")
            widget_cb(r)

        # GENERAL SETTINGS
        section("GENERAL SETTINGS")

        current_theme = self._settings.get("theme", "Default")
        self._theme_var = tk.StringVar(value=current_theme)

        def make_theme_row(r):
            mb = tk.Menubutton(r, textvariable=self._theme_var,
                               bg=T.PANEL, fg=T.AMBER,
                               activebackground=T.PANEL, activeforeground=T.AMBER_BRIGHT,
                               font=T.best_font(8), relief="flat", bd=1,
                               highlightthickness=1, highlightbackground=T.BORDER)
            menu = tk.Menu(mb, tearoff=False, bg=T.PANEL, fg=T.AMBER,
                           activebackground=T.BORDER_DIM, activeforeground=T.AMBER_BRIGHT,
                           font=T.best_font(8))
            for name in T.THEME_NAMES:
                menu.add_command(label=name,
                                 command=lambda n=name: self._set_theme(n))
            mb.configure(menu=menu)
            mb.pack(side="left")

        row("TOOL THEME", make_theme_row)

        current_ms  = self._settings.get("poll_interval_ms", 15 * 60 * 1000)
        current_lbl = next((l for l, ms in POLL_OPTIONS if ms == current_ms), "15 MIN")
        self._poll_var = tk.StringVar(value=current_lbl)

        def make_poll_row(r):
            mb = tk.Menubutton(r, textvariable=self._poll_var,
                               bg=T.PANEL, fg=T.AMBER,
                               activebackground=T.PANEL, activeforeground=T.AMBER_BRIGHT,
                               font=T.best_font(8), relief="flat", bd=1,
                               highlightthickness=1, highlightbackground=T.BORDER)
            menu = tk.Menu(mb, tearoff=False, bg=T.PANEL, fg=T.AMBER,
                           activebackground=T.BORDER_DIM, activeforeground=T.AMBER_BRIGHT,
                           font=T.best_font(8))
            for lbl, ms in POLL_OPTIONS:
                menu.add_command(label=lbl, command=lambda l=lbl, m=ms: self._set_poll(l, m))
            mb.configure(menu=menu)
            mb.pack(side="left")

        row("POLL INTERVAL", make_poll_row)

        self._startup_var = tk.BooleanVar(value=_get_startup())

        def make_startup_row(r):
            def toggle():
                _set_startup(self._startup_var.get())
            tk.Checkbutton(r, variable=self._startup_var, command=toggle,
                           bg=T.BG, fg=T.AMBER_DIM,
                           activebackground=T.BG, activeforeground=T.AMBER,
                           selectcolor=T.PANEL,
                           relief="flat", bd=0).pack(side="left")

        row("LAUNCH ON STARTUP", make_startup_row)

        # Helper — creates a checkbox row callback bound to a settings key
        def _ck(key, default):
            def _make(r):
                var = tk.BooleanVar(value=self._settings.get(key, default))
                def toggle(k=key, v=var):
                    self._settings[k] = v.get()
                    if cb := self._settings.get("_on_colour_change_cb"):
                        cb()
                tk.Checkbutton(r, variable=var, command=toggle,
                               bg=T.BG, fg=T.AMBER_DIM,
                               activebackground=T.BG, activeforeground=T.AMBER,
                               selectcolor=T.PANEL,
                               relief="flat", bd=0).pack(side="left")
            return _make

        # FLOATING WIDGET SETTINGS
        section("FLOATING WIDGET SETTINGS")
        row("TRANSPARENT BG", _ck("float_transparent_bg", False))
        row("TEXT F/X",       _ck("float_text_fx",        True))

        # TASKBAR WIDGET SETTINGS
        section("TASKBAR WIDGET SETTINGS")
        row("TRANSPARENT BG", _ck("taskbar_transparent_bg", False))
        row("TEXT F/X",       _ck("taskbar_text_fx",        True))

        # ABOUT
        section("ABOUT")

        def lbl_row(label, value, colour=None):
            r = tk.Frame(frame, bg=T.BG)
            r.pack(fill="x", padx=10, pady=1)
            tk.Label(r, text=label, bg=T.BG, fg=T.AMBER_DIM,
                     font=T.best_font(8), width=18, anchor="w").pack(side="left")
            tk.Label(r, text=value, bg=T.BG,
                     fg=colour or T.AMBER,
                     font=T.best_font(8)).pack(side="left")

        lbl_row("VERSION", VERSION, T.AMBER_BRIGHT)
        lbl_row("AUTHORS", "CHRIS CARPENTER")
        lbl_row("",        "CLAUDE SONNET 4.6")

        r = tk.Frame(frame, bg=T.BG)
        r.pack(fill="x", padx=10, pady=1)
        tk.Label(r, text="REPOSITORY", bg=T.BG, fg=T.AMBER_DIM,
                 font=T.best_font(8), width=18, anchor="w").pack(side="left")
        link = tk.Label(r, text="github: Godimas101/personal-projects", bg=T.BG, fg=T.AMBER,
                        font=T.best_font(8), cursor="hand2")
        link.pack(side="left")
        link.bind("<Button-1>", lambda _: _open_url(REPO_URL))
        link.bind("<Enter>",    lambda _: link.configure(fg=T.AMBER_BRIGHT))
        link.bind("<Leave>",    lambda _: link.configure(fg=T.AMBER))

        tk.Frame(frame, bg=T.BG, height=12).pack()
        return frame

    # ── Supporters tab ────────────────────────────────────────────────────────

    def _build_supporters(self, parent) -> tk.Frame:
        frame = tk.Frame(parent, bg=T.BG)

        tk.Frame(frame, bg=T.BORDER, height=1).pack(fill="x", padx=10, pady=(10, 0))
        tk.Label(frame, text="OUR SUPPORTERS", bg=T.BG, fg=T.AMBER,
                 font=T.best_font(8, bold=True)).pack(anchor="w", padx=10, pady=(4, 0))
        tk.Label(frame,
                 text="These folks help keep the tools free. Thank you \u2665",
                 bg=T.BG, fg=T.AMBER_DIM,
                 font=T.best_font(8)).pack(anchor="w", padx=10, pady=(2, 6))

        # Scrollable list
        list_frame = tk.Frame(frame, bg=T.BG)
        list_frame.pack(fill="both", expand=True, padx=(10, 0))

        canvas = tk.Canvas(list_frame, bg=T.BG, bd=0, highlightthickness=0)

        from tkinter import ttk as _ttk
        _style = _ttk.Style(list_frame)
        _style.theme_use("clam")
        _style.configure("Monitor.Vertical.TScrollbar",
            background=T.BORDER,
            troughcolor=T.BG,
            arrowcolor=T.AMBER_DIM,
            darkcolor=T.PANEL,
            lightcolor=T.BORDER,
            bordercolor=T.BG,
            gripcount=0)
        _style.map("Monitor.Vertical.TScrollbar",
            background=[("active", T.AMBER), ("!active", T.BORDER)])

        vsb = _ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview,
                             style="Monitor.Vertical.TScrollbar")
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y", padx=(0, 6))
        canvas.pack(side="left", fill="both", expand=True)

        self._supporters_inner = tk.Frame(canvas, bg=T.BG)
        self._supporters_win   = canvas.create_window(
            (0, 0), window=self._supporters_inner, anchor="nw")

        def _on_frame(*_):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def _on_canvas(e):
            canvas.itemconfig(self._supporters_win, width=e.width)

        self._supporters_inner.bind("<Configure>", _on_frame)
        canvas.bind("<Configure>", _on_canvas)

        self._supporters_status = tk.Label(
            self._supporters_inner,
            text="Loading\u2026",
            bg=T.BG, fg=T.AMBER_DIM,
            font=T.best_font(8))
        self._supporters_status.pack(anchor="w", padx=4, pady=4)

        # Footer
        tk.Frame(frame, bg=T.BORDER, height=1).pack(fill="x", padx=10, pady=(6, 0))
        foot = tk.Frame(frame, bg=T.BG)
        foot.pack(fill="x", padx=10, pady=(6, 10))
        tk.Button(foot, text="SUPPORT ON PATREON",
                  bg=T.PANEL, fg=T.AMBER_BRIGHT,
                  activebackground=T.BORDER_DIM, activeforeground=T.AMBER_BRIGHT,
                  font=T.best_font(8, bold=True),
                  relief="flat", bd=0, padx=10, pady=4, cursor="hand2",
                  highlightthickness=1, highlightbackground=T.AMBER,
                  command=lambda: _open_url(PATREON_URL)).pack(side="left")

        threading.Thread(target=self._fetch_supporters, daemon=True).start()
        return frame

    def _fetch_supporters(self):
        try:
            req = urllib.request.Request(
                SUPPORTERS_URL,
                headers={"Cache-Control": "no-cache",
                         "User-Agent": "ClaudeUsageMonitor/1.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode())
            self.after(0, lambda: self._populate_supporters(data))
        except Exception as exc:
            self.after(0, lambda: self._supporters_status.configure(
                text=f"Could not load: {exc}", fg=T.AMBER_DIM))

    def _populate_supporters(self, data):
        if not self.winfo_exists():
            return
        self._supporters_status.destroy()

        tiers = data.get("tiers", [])
        if not tiers or not any(t.get("members") for t in tiers):
            tk.Label(self._supporters_inner,
                     text="No supporters yet \u2014 be the first!",
                     bg=T.BG, fg=T.AMBER_DIM,
                     font=T.best_font(8)).pack(anchor="w", padx=4, pady=4)
            return

        for tier in tiers:
            members = tier.get("members", [])
            if not members:
                continue
            tk.Label(self._supporters_inner,
                     text=tier.get("tier", "Supporters"),
                     bg=T.BG, fg=T.AMBER_BRIGHT,
                     font=T.best_font(8, bold=True)).pack(
                         anchor="w", padx=4, pady=(8, 2))
            tk.Frame(self._supporters_inner, bg=T.BORDER, height=1).pack(
                fill="x", pady=(0, 4))
            for name in members:
                tk.Label(self._supporters_inner,
                         text=f"  \u2713  {name}",
                         bg=T.BG, fg=T.AMBER,
                         font=T.best_font(8)).pack(anchor="w", padx=4)

    def _set_poll(self, label: str, ms: int):
        self._poll_var.set(label)
        self._settings["poll_interval_ms"] = ms
        if self._on_change:
            self._on_change()

    def _set_theme(self, name: str):
        self._theme_var.set(name)
        self._settings["theme"] = name
        T.apply_theme(name)
        if cb := self._settings.get("_on_colour_change_cb"):
            cb()
        self._rebuild()

    # ── Nerds Only tab — 2-column fixed layout ────────────────────────────────

    def _build_nerds(self, parent) -> tk.Frame:
        outer = tk.Frame(parent, bg=T.BG)

        # Two-column area
        cols = tk.Frame(outer, bg=T.BG)
        cols.pack(fill="both", expand=True)

        self._nerds_left = tk.Frame(cols, bg=T.BG)
        self._nerds_left.pack(side="left", fill="both", expand=True, padx=0)

        tk.Frame(cols, bg=T.BORDER, width=1).pack(side="left", fill="y")

        self._nerds_right = tk.Frame(cols, bg=T.BG)
        self._nerds_right.pack(side="left", fill="y", padx=0)

        self._populate_nerds_left(self._nerds_left)
        self._populate_nerds_right(self._nerds_right)

        # Refresh button
        tk.Frame(outer, bg=T.BORDER, height=1).pack(fill="x", padx=8, pady=(8, 0))

        def refresh():
            threading.Thread(target=self._refresh_nerds, daemon=True).start()

        tk.Button(outer, text="↺  REFRESH STATS",
                  bg=T.PANEL, fg=T.AMBER,
                  activebackground=T.BORDER_DIM, activeforeground=T.AMBER_BRIGHT,
                  font=T.best_font(8), relief="flat", bd=0,
                  cursor="hand2", padx=10, pady=4,
                  command=refresh).pack(pady=(4, 10))

        return outer

    def _populate_nerds_left(self, frame: tk.Frame):
        rate  = self._rate_data
        local = self._local

        def section(text):
            tk.Frame(frame, bg=T.BORDER, height=1).pack(fill="x", padx=8, pady=(8, 0))
            tk.Label(frame, text=text, bg=T.BG, fg=T.AMBER,
                     font=T.best_font(8, bold=True)).pack(anchor="w", padx=8, pady=(4, 2))

        def stat(label, value, colour=None):
            r = tk.Frame(frame, bg=T.BG)
            r.pack(fill="x", padx=8, pady=1)
            tk.Label(r, text=label, bg=T.BG, fg=T.AMBER_DIM,
                     font=T.best_font(8), width=14, anchor="w").pack(side="left")
            tk.Label(r, text=str(value).upper(), bg=T.BG,
                     fg=colour or T.AMBER_BRIGHT,
                     font=T.best_font(8)).pack(side="left")

        def bar_stat(label, pct, countdown):
            r = tk.Frame(frame, bg=T.BG)
            r.pack(fill="x", padx=8, pady=2)
            tk.Label(r, text=label, bg=T.BG, fg=T.AMBER_DIM,
                     font=T.best_font(7), width=14, anchor="w").pack(side="left")
            tk.Label(r, text=T.render_bar(pct / 100, 8),
                     bg=T.BG, fg=T.usage_colour(pct / 100),
                     font=T.best_font(7)).pack(side="left")
            tk.Label(r, text=f" {int(pct)}%  {countdown}",
                     bg=T.BG, fg=T.AMBER, font=T.best_font(7)).pack(side="left")

        # RATE LIMITS
        section("RATE LIMITS")
        if rate:
            for key, win in rate.windows.items():
                bar_stat(key.upper().replace("_", " "), win.pct, win.countdown)
        else:
            stat("STATUS", "NO DATA — CHECK CREDENTIALS", T.RED)

        # BURN RATE
        section("BURN RATE")
        if local:
            stat("TOK/MIN",  f"{local.burn_rate:,.0f}",
                 T.usage_colour(local.burn_rate / 3000))
            stat("VELOCITY", local.velocity)

        # MODEL BREAKDOWN
        section("MODEL BREAKDOWN")
        if local and local.model_pct:
            for model, pct in sorted(local.model_pct.items(), key=lambda x: -x[1]):
                stat(model.upper()[:14], f"{pct * 100:.1f}%")
        elif local:
            stat("STATUS", "NO DATA YET", T.AMBER_DIM)

        # Claude Code mascot — centered in remaining space
        _MASCOT = (
            "   ▐▛███▜▌\n"
            "   ▝▜██████▛▘\n"
            "   ▘▘ ▝▝"
        )
        spacer = tk.Frame(frame, bg=T.BG)
        spacer.pack(fill="both", expand=True)
        tk.Label(spacer, text=_MASCOT, bg=T.BG, fg=T.AMBER_DIM,
                 font=T.best_font(8), justify="center").pack(expand=True)

        # Bottom padding
        tk.Frame(frame, bg=T.BG, height=8).pack()

    def _populate_nerds_right(self, frame: tk.Frame):
        local = self._local

        def section(text):
            tk.Frame(frame, bg=T.BORDER, height=1).pack(fill="x", padx=8, pady=(8, 0))
            tk.Label(frame, text=text, bg=T.BG, fg=T.AMBER,
                     font=T.best_font(8, bold=True)).pack(anchor="w", padx=8, pady=(4, 2))

        def stat(label, value, colour=None):
            r = tk.Frame(frame, bg=T.BG)
            r.pack(fill="x", padx=8, pady=1)
            tk.Label(r, text=label, bg=T.BG, fg=T.AMBER_DIM,
                     font=T.best_font(8), width=14, anchor="w").pack(side="left")
            tk.Label(r, text=str(value).upper(), bg=T.BG,
                     fg=colour or T.AMBER_BRIGHT,
                     font=T.best_font(8)).pack(side="left")

        # TODAY
        section("TODAY")
        if local:
            t = local.today
            stat("MESSAGES",   f"{t.messages:,}")
            stat("OUTPUT",     T.fmt_tokens(t.output_tokens))
            stat("INPUT",      T.fmt_tokens(t.input_tokens))
            stat("CACHE READ", T.fmt_tokens(t.cache_read))
            stat("CACHE WRITE", T.fmt_tokens(t.cache_create))
            stat("COST (USD)", f"${t.cost_usd:.4f}")
        else:
            stat("STATUS", "NO LOCAL DATA", T.AMBER_DIM)

        # SESSION
        section("SESSION (5H BLOCK)")
        if local:
            s = local.session
            stat("MESSAGES",   f"{s.messages:,}")
            stat("OUTPUT",     T.fmt_tokens(s.output_tokens))
            stat("INPUT",      T.fmt_tokens(s.input_tokens))
            stat("COST (USD)", f"${s.cost_usd:.4f}")

        # ALL TIME
        section("ALL TIME")
        if local:
            a = local.all_time
            stat("MESSAGES",   f"{a.messages:,}")
            stat("OUTPUT",     T.fmt_tokens(a.output_tokens))
            stat("INPUT",      T.fmt_tokens(a.input_tokens))
            stat("TOTAL",      T.fmt_tokens(a.total_tokens))
            stat("COST (USD)", f"${a.cost_usd:.2f}")
            if a.timestamps:
                first = min(a.timestamps)
                stat("FIRST USE",  first.strftime("%Y-%m-%d"))

        # Bottom padding
        tk.Frame(frame, bg=T.BG, height=8).pack()

    def _refresh_nerds(self):
        rate  = usage_reader.fetch_rate_limits()
        local = usage_reader.scan_local()
        self._rate_data = rate
        self._local     = local

        def update():
            for w in self._nerds_left.winfo_children():
                w.destroy()
            for w in self._nerds_right.winfo_children():
                w.destroy()
            self._populate_nerds_left(self._nerds_left)
            self._populate_nerds_right(self._nerds_right)

        self.after(0, update)

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _center(self, parent):
        self.update_idletasks()
        pw = self.winfo_width()
        ph = self.winfo_height()
        sw = parent.winfo_screenwidth()
        sh = parent.winfo_screenheight()
        # Use rootx/rooty for screen-absolute coords (works when parent is embedded)
        rx = parent.winfo_rootx()
        ry = parent.winfo_rooty()
        px = rx + (parent.winfo_width() - pw) // 2
        # Open above parent; fall back to below if off-screen
        py = ry - ph - 4
        if py < 0:
            py = ry + parent.winfo_height() + 4
        px = max(0, min(px, sw - pw))
        py = max(0, min(py, sh - ph))
        self.geometry(f"+{px}+{py}")


# ── Startup registry helpers ──────────────────────────────────────────────────

_REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"


def _get_startup() -> bool:
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, _REG_PATH) as key:
            winreg.QueryValueEx(key, APP_NAME)
            return True
    except FileNotFoundError:
        return False
    except Exception:
        return False


def _set_startup(enabled: bool) -> None:
    import pathlib
    exe_path = pathlib.Path(sys.executable)
    # Always use pythonw.exe — python.exe opens a console window at startup
    # which kills the monitor when the user closes it
    if exe_path.stem.lower() == "python":
        pw = exe_path.parent / "pythonw.exe"
        if pw.exists():
            exe_path = pw
    exe    = str(exe_path)
    script = str(pathlib.Path(__file__).resolve().parent / "main.py")
    cmd    = f'"{exe}" "{script}"'
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, _REG_PATH,
                            0, winreg.KEY_SET_VALUE) as key:
            if enabled:
                winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, cmd)
            else:
                try:
                    winreg.DeleteValue(key, APP_NAME)
                except FileNotFoundError:
                    pass
    except Exception:
        pass


def _open_url(url: str) -> None:
    import webbrowser
    webbrowser.open(url)
