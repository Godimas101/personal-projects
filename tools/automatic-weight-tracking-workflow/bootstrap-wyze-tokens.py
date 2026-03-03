"""
bootstrap-wyze-tokens.py
Run this locally (residential IP) to do a fresh Wyze login and push the
resulting tokens to the server's .env.

Only needed if the rolling token chain breaks (server offline > 28 days).
Normal operation: get_wyze_data.py self-refreshes on every run.

Usage:
  python bootstrap-wyze-tokens.py              # print sed commands only
  python bootstrap-wyze-tokens.py --push       # SSH and update server .env automatically
"""

import argparse
import subprocess
import sys
from wyze_sdk import Client

try:
    from credentials import EMAIL, PASSWORD, KEY_ID, API_KEY, SERVER
except ImportError:
    print("ERROR: credentials.py not found.")
    print("Copy credentials.example.py to credentials.py and fill in your values.")
    sys.exit(1)
ENV_FILE = '/root/n8n-docker-caddy/.env'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--push', action='store_true', help='SSH and update server .env directly')
    args = parser.parse_args()

    print("Logging in to Wyze (from local machine)...")
    try:
        client = Client(email=EMAIL, password=PASSWORD, key_id=KEY_ID, api_key=API_KEY)
    except Exception as e:
        print(f"Login failed: {e}")
        sys.exit(1)

    access  = client._token
    refresh = client._refresh_token
    print("Login successful.\n")

    sed_access  = f"sed -i 's|^WYZE_ACCESS_TOKEN=.*|WYZE_ACCESS_TOKEN={access}|' {ENV_FILE}"
    # Use grep to add WYZE_REFRESH_TOKEN if it doesn't exist, otherwise sed
    sed_refresh = (
        f"grep -q '^WYZE_REFRESH_TOKEN=' {ENV_FILE} "
        f"&& sed -i 's|^WYZE_REFRESH_TOKEN=.*|WYZE_REFRESH_TOKEN={refresh}|' {ENV_FILE} "
        f"|| echo 'WYZE_REFRESH_TOKEN={refresh}' >> {ENV_FILE}"
    )

    if args.push:
        print(f"Pushing tokens to {SERVER}...")
        for cmd in [sed_access, sed_refresh]:
            result = subprocess.run(
                ['ssh', '-o', 'StrictHostKeyChecking=no', '-o', 'BatchMode=yes', SERVER, cmd],
                capture_output=True, text=True, stdin=subprocess.DEVNULL
            )
            if result.returncode != 0:
                print(f"SSH error: {result.stderr}")
                sys.exit(1)
        print("Done! Tokens updated on server.")
        print("\nRestart n8n to reload .env:")
        print(f"  ssh {SERVER} 'cd /root/n8n-docker-caddy && docker compose restart n8n'")
    else:
        print("Run these commands on the server, or re-run with --push to do it automatically:\n")
        print(sed_access)
        print(sed_refresh)

if __name__ == "__main__":
    main()
