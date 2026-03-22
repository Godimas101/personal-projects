# usage_reader.py — OAuth API + local JSONL data layer
# Zero external dependencies — pure Python stdlib

import json
import pathlib
import subprocess
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone
from typing import Optional

# ── Paths ─────────────────────────────────────────────────────────────────────
CREDENTIALS_PATH = pathlib.Path.home() / ".claude" / ".credentials.json"
PROJECTS_PATH    = pathlib.Path.home() / ".claude" / "projects"
ALT_PROJECTS     = pathlib.Path.home() / ".config" / "claude" / "projects"

# ── API ───────────────────────────────────────────────────────────────────────
USAGE_API_URL = "https://api.anthropic.com/api/oauth/usage"
API_BETA      = "oauth-2025-04-20"

# ── Model pricing per 1M tokens (USD): input, output, cache_create, cache_read
MODEL_PRICING = {
    "claude-opus-4":     (15.00, 75.00, 18.75, 1.50),
    "claude-sonnet-4":   ( 3.00, 15.00,  3.75, 0.30),
    "claude-haiku-4":    ( 0.80,  4.00,  1.00, 0.08),
    "claude-opus-4-5":   (15.00, 75.00, 18.75, 1.50),
    "claude-sonnet-4-6": ( 3.00, 15.00,  3.75, 0.30),
    "claude-haiku-4-5":  ( 0.80,  4.00,  1.00, 0.08),
    "default":           ( 3.00, 15.00,  3.75, 0.30),
}


# ── Credentials ───────────────────────────────────────────────────────────────

def _get_token() -> Optional[str]:
    try:
        with open(CREDENTIALS_PATH, encoding="utf-8") as f:
            data = json.load(f)
        return data.get("claudeAiOauth", {}).get("accessToken")
    except Exception:
        return None


def _refresh_token() -> bool:
    """Shell out to the Claude CLI to refresh an expired token."""
    for cmd in (["claude.cmd", "-p", "."], ["claude", "-p", "."]):
        try:
            subprocess.run(
                cmd,
                capture_output=True,
                timeout=30,
                creationflags=0x08000000,  # CREATE_NO_WINDOW
            )
            return True
        except Exception:
            continue
    return False


# ── OAuth API ─────────────────────────────────────────────────────────────────

def _do_fetch(token: str) -> Optional[dict]:
    try:
        req = urllib.request.Request(
            USAGE_API_URL,
            headers={
                "Authorization": f"Bearer {token}",
                "anthropic-beta": API_BETA,
            },
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            return None  # token expired — caller will refresh
        return None
    except Exception:
        return None


def fetch_rate_limits() -> Optional["RateLimitData"]:
    """Fetch live 5h/7d rate limit data from Anthropic API.
    Returns None on failure (network down, no credentials, etc.)."""
    token = _get_token()
    if not token:
        return None
    raw = _do_fetch(token)
    if raw is None:
        # Attempt token refresh then retry once
        if _refresh_token():
            token = _get_token()
            if token:
                raw = _do_fetch(token)
    if raw is None:
        return None
    return RateLimitData(raw)


# ── Rate limit data model ─────────────────────────────────────────────────────

def _parse_dt(s: str) -> Optional[datetime]:
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:
        return None


def _countdown(reset_at: Optional[datetime]) -> str:
    if reset_at is None:
        return "?"
    delta = reset_at - datetime.now(timezone.utc)
    secs  = int(delta.total_seconds())
    if secs <= 0:
        return "SOON"
    days  = secs // 86400
    hours = (secs % 86400) // 3600
    mins  = (secs % 3600) // 60
    if days:   return f"{days}D {hours}H"
    if hours:  return f"{hours}H {mins}M"
    return f"{mins}M"


class WindowData:
    __slots__ = ("pct", "reset_at", "countdown")

    def __init__(self, raw: dict):
        self.pct      = float(raw.get("utilization") or 0)
        self.reset_at = _parse_dt(raw.get("resets_at", ""))
        self.countdown = _countdown(self.reset_at)


class RateLimitData:
    def __init__(self, raw: dict):
        self.windows: dict[str, WindowData] = {}
        for key, val in raw.items():
            if isinstance(val, dict) and "utilization" in val:
                self.windows[key] = WindowData(val)

    def _w(self, key: str) -> Optional[WindowData]:
        return self.windows.get(key)

    @property
    def five_hour(self) -> Optional[WindowData]:
        return self._w("five_hour")

    @property
    def seven_day(self) -> Optional[WindowData]:
        return self._w("seven_day")

    @property
    def five_hour_pct(self) -> float:
        w = self.five_hour
        return w.pct if w else 0.0

    @property
    def seven_day_pct(self) -> float:
        w = self.seven_day
        return w.pct if w else 0.0

    def _time_frac(self, window_key: str, total_seconds: float) -> float:
        """Fraction of the time window elapsed (0=just reset, 1=about to reset)."""
        w = self._w(window_key)
        if not w or w.reset_at is None:
            return 0.0
        remaining = (w.reset_at - datetime.now(timezone.utc)).total_seconds()
        elapsed   = total_seconds - remaining
        return max(0.0, min(1.0, elapsed / total_seconds))

    @property
    def five_hour_time_frac(self) -> float:
        return self._time_frac("five_hour", 5 * 3600)

    @property
    def seven_day_time_frac(self) -> float:
        return self._time_frac("seven_day", 7 * 24 * 3600)

    @property
    def five_hour_countdown(self) -> str:
        w = self.five_hour
        return w.countdown if w else "?"

    @property
    def seven_day_countdown(self) -> str:
        w = self.seven_day
        return w.countdown if w else "?"


# ── Local JSONL stats ─────────────────────────────────────────────────────────

def _projects_dir() -> Optional[pathlib.Path]:
    if PROJECTS_PATH.exists():
        return PROJECTS_PATH
    if ALT_PROJECTS.exists():
        return ALT_PROJECTS
    return None


def _iter_records():
    """Yield every parsed JSON record from all project JSONL files."""
    d = _projects_dir()
    if d is None:
        return
    for f in d.rglob("*.jsonl"):
        try:
            with open(f, encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        yield json.loads(line)
                    except json.JSONDecodeError:
                        continue
        except Exception:
            continue


def _normalize_model(model: str) -> str:
    m = model.lower()
    for key in MODEL_PRICING:
        if key in m:
            return key
    return "default"


def _extract_usage(record: dict) -> Optional[dict]:
    """Pull the usage dict from whatever structure this record uses."""
    # Direct usage key
    if "usage" in record and isinstance(record["usage"], dict):
        return record["usage"]
    # Nested under message
    msg = record.get("message", {})
    if isinstance(msg, dict) and "usage" in msg:
        return msg["usage"]
    return None


def _extract_model(record: dict) -> str:
    if "model" in record:
        return record["model"]
    msg = record.get("message", {})
    if isinstance(msg, dict):
        return msg.get("model", "default")
    return "default"


def _extract_ts(record: dict) -> Optional[datetime]:
    for key in ("timestamp", "created_at", "ts"):
        raw = record.get(key)
        if raw:
            try:
                return datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
            except Exception:
                continue
    return None


class UsageStats:
    """Aggregated token usage for a time window."""
    __slots__ = (
        "messages", "input_tokens", "output_tokens",
        "cache_create", "cache_read", "cost_usd",
        "model_output", "timestamps",
    )

    def __init__(self):
        self.messages      = 0
        self.input_tokens  = 0
        self.output_tokens = 0
        self.cache_create  = 0
        self.cache_read    = 0
        self.cost_usd      = 0.0
        self.model_output: dict[str, int] = {}
        self.timestamps: list[datetime]   = []

    def add(self, record: dict) -> None:
        usage = _extract_usage(record)
        if not usage:
            return
        inp = usage.get("input_tokens", 0) or 0
        out = usage.get("output_tokens", 0) or 0
        cc  = usage.get("cache_creation_input_tokens", 0) or 0
        cr  = usage.get("cache_read_input_tokens", 0) or 0
        if inp == 0 and out == 0:
            return  # skip empty records

        model   = _normalize_model(_extract_model(record))
        pricing = MODEL_PRICING.get(model, MODEL_PRICING["default"])

        self.messages      += 1
        self.input_tokens  += inp
        self.output_tokens += out
        self.cache_create  += cc
        self.cache_read    += cr
        self.cost_usd      += (inp * pricing[0] + out * pricing[1] +
                               cc  * pricing[2] + cr  * pricing[3]) / 1_000_000
        self.model_output[model] = self.model_output.get(model, 0) + out

        ts = _extract_ts(record)
        if ts:
            self.timestamps.append(ts)

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens + self.cache_create + self.cache_read


class LocalStats:
    """All aggregated stats from local JSONL files."""

    def __init__(self):
        self.all_time:   UsageStats = UsageStats()
        self.today:      UsageStats = UsageStats()
        self.session:    UsageStats = UsageStats()  # current 5-hour block
        self.burn_rate:  float      = 0.0           # output tokens / minute
        self.velocity:   str        = "IDLE"
        self.model_pct:  dict       = {}            # model → fraction of output

    def _compute_derived(self) -> None:
        now = datetime.now(timezone.utc)

        # Burn rate from today's data
        if self.today.timestamps and self.today.output_tokens > 0:
            oldest = min(self.today.timestamps)
            elapsed = max(1.0, (now - oldest).total_seconds() / 60)
            self.burn_rate = self.today.output_tokens / elapsed

        # Velocity label
        br = self.burn_rate
        if   br == 0:      self.velocity = "IDLE"
        elif br < 500:     self.velocity = "SLOW"
        elif br < 1_500:   self.velocity = "NORMAL"
        elif br < 3_000:   self.velocity = "FAST"
        else:              self.velocity = "VERY FAST"

        # Model distribution
        total = sum(self.all_time.model_output.values()) or 1
        self.model_pct = {
            k: v / total for k, v in self.all_time.model_output.items()
        }


def scan_local() -> LocalStats:
    """Scan all JSONL files and return aggregated stats."""
    stats = LocalStats()
    now   = datetime.now(timezone.utc)

    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    hour_block  = (now.hour // 5) * 5
    sess_start  = now.replace(hour=hour_block, minute=0, second=0, microsecond=0)

    for record in _iter_records():
        stats.all_time.add(record)
        ts = _extract_ts(record)
        if ts is not None:
            if ts >= today_start:
                stats.today.add(record)
            if ts >= sess_start:
                stats.session.add(record)

    stats._compute_derived()
    return stats
