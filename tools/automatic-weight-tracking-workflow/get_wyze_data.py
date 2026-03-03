"""
get_wyze_data.py
Fetches the latest Wyze Scale measurement and prints JSON to stdout.
Called by n8n via SSH node.

Self-refreshing: loads tokens from .env, calls refresh_token() (not blocked
from datacenter IPs), writes new tokens back to .env, then fetches scale data.
The rolling refresh means the token chain never expires as long as this script
runs at least once every 28 days.

Output format (success):
  {"data": {<all ScaleRecord fields>}}
  Fields include: weight (lbs), body_fat, bmi, bmr, muscle, body_water,
  bone_mineral, body_vfr, protein, metabolic_age, measure_ts, timezone, etc.

Output format (failure):
  {"error": "<message>"}
"""

import json
import os
import re
import sys
from datetime import datetime, timedelta
from wyze_sdk import Client

ENV_FILE = '/root/n8n-docker-caddy/.env'


def load_env_tokens():
    """Read all required Wyze credentials from the .env file."""
    keys = {}
    try:
        with open(ENV_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                for key in ('WYZE_ACCESS_TOKEN', 'WYZE_REFRESH_TOKEN', 'WYZE_KEY_ID', 'WYZE_API_KEY'):
                    if line.startswith(key + '='):
                        keys[key] = line.split('=', 1)[1].strip()
    except Exception as e:
        print(json.dumps({"error": f"Could not read {ENV_FILE}: {e}"}))
        sys.exit(1)

    missing = [k for k in ('WYZE_ACCESS_TOKEN', 'WYZE_REFRESH_TOKEN', 'WYZE_KEY_ID', 'WYZE_API_KEY') if not keys.get(k)]
    if missing:
        print(json.dumps({"error": f"Missing from .env: {', '.join(missing)}"}))
        sys.exit(1)

    return keys['WYZE_ACCESS_TOKEN'], keys['WYZE_REFRESH_TOKEN'], keys['WYZE_KEY_ID'], keys['WYZE_API_KEY']


def save_env_tokens(new_access, new_refresh):
    """Write updated tokens back to the .env file in-place."""
    try:
        with open(ENV_FILE, 'r') as f:
            content = f.read()

        # Replace existing token lines (or append if missing)
        for key, value in [('WYZE_ACCESS_TOKEN', new_access), ('WYZE_REFRESH_TOKEN', new_refresh)]:
            pattern = rf'^{key}=.*$'
            replacement = f'{key}={value}'
            if re.search(pattern, content, flags=re.MULTILINE):
                content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
            else:
                content = content.rstrip('\n') + f'\n{replacement}\n'

        with open(ENV_FILE, 'w') as f:
            f.write(content)
    except Exception as e:
        # Non-fatal — log to stderr but don't abort; we still have a valid token this run
        print(f"WARNING: Could not write refreshed tokens to {ENV_FILE}: {e}", file=sys.stderr)


def main():
    access_token, refresh_token, key_id, api_key = load_env_tokens()

    # Init client with stored tokens — no login call, not blocked from server
    client = Client(token=access_token, refresh_token=refresh_token,
                    key_id=key_id, api_key=api_key)

    # Refresh the token (uses /app/user/refresh_token — not IP-blocked)
    # Also rotates the refresh_token itself, so the chain never expires
    try:
        client.refresh_token()
        save_env_tokens(client._token, client._refresh_token)
    except Exception as e:
        # If refresh fails, continue with the existing token — it may still be valid
        print(f"WARNING: Token refresh failed: {e}", file=sys.stderr)

    # Fetch records for the last 2 days to handle timezone edge cases
    end_time   = datetime.now()
    start_time = end_time - timedelta(days=2)

    try:
        records = client.scales.get_records(start_time=start_time, end_time=end_time)
    except Exception as e:
        print(json.dumps({"error": f"get_records failed: {e}"}))
        sys.exit(1)

    if not records:
        print(json.dumps({"error": "No records returned. Step on the scale first, or confirm it is shared to this account."}))
        sys.exit(1)

    latest = sorted(records, key=lambda r: r.measure_ts, reverse=True)[0]

    # Dump everything available on the record object
    record_data = {}
    for attr in dir(latest):
        if attr.startswith('_'):
            continue
        try:
            val = getattr(latest, attr)
            if callable(val):
                continue
            # Convert to JSON-safe type
            record_data[attr] = val
        except Exception:
            pass

    print(json.dumps({"data": record_data}, default=str))


if __name__ == "__main__":
    main()
