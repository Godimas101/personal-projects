"""
refresh-wyze-token.py
─────────────────────
Gets a fresh Wyze access token via wyze-sdk and prints the exact commands
to update your n8n server. Run this every ~2 days when the access token expires.

Usage:
  python refresh-wyze-token.py
  python refresh-wyze-token.py --push   (auto-SSH to update server, requires ssh key)

Setup for --push:
  Set SERVER below to your droplet IP or hostname.
  Ensure you can SSH without password (ssh-copy-id root@yourserver or key in ssh-agent).
"""

import sys
import subprocess

# ── Config ────────────────────────────────────────────────────────────────────
EMAIL    = "aeneas.carpenter@gmail.com"
PASSWORD = "WyzeP@ssword"
KEY_ID   = "22927812-6a45-4148-8564-ea86679df596"
API_KEY  = "3vQpzlbdi9QJUyK5HxiM2gn9Qv2Hw4CXmcIQxNqZ6hPHm6PqwlZozhKTnL7P"
USER_ID  = "f99829c9c6a34a4597257e90d9802a21"

# Your DigitalOcean droplet — update if IP changes
SERVER   = "root@n8n.thecanadian.space"
ENV_FILE = "/root/n8n-docker-caddy/.env"
COMPOSE_DIR = "/root/n8n-docker-caddy"

# ─────────────────────────────────────────────────────────────────────────────

def get_token():
    try:
        from wyze_sdk import Client
        from wyze_sdk.errors import WyzeApiError
    except ImportError:
        print("ERROR: wyze-sdk not installed. Run: pip install wyze-sdk")
        sys.exit(1)

    print("Authenticating with Wyze...")
    try:
        client = Client()
        response = client.login(email=EMAIL, password=PASSWORD, key_id=KEY_ID, api_key=API_KEY)
        data = response.data if hasattr(response, 'data') else response
        access_token = data.get('access_token') or data.get('accessToken', '')
        if not access_token:
            print("ERROR: No access_token in response:", dict(data))
            sys.exit(1)
        print("Login successful!")
        return access_token
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


def push_to_server(access_token):
    """SSH into the server, update WYZE_ACCESS_TOKEN in .env, restart n8n."""
    print(f"\nPushing to {SERVER}...")

    # Use sed to replace the WYZE_ACCESS_TOKEN line in .env
    sed_cmd = f"sed -i 's|^WYZE_ACCESS_TOKEN=.*|WYZE_ACCESS_TOKEN={access_token}|' {ENV_FILE}"
    restart_cmd = f"cd {COMPOSE_DIR} && docker compose down && docker compose up -d"
    full_cmd = f"{sed_cmd} && {restart_cmd}"

    result = subprocess.run(
        ["ssh", "-o", "StrictHostKeyChecking=no", SERVER, full_cmd],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print("Server updated and n8n restarted successfully!")
    else:
        print("SSH failed:")
        print(result.stderr)
        print("\nFall back to manual steps below.")
        return False
    return True


def print_manual_steps(access_token):
    print("\n" + "─" * 70)
    print("MANUAL UPDATE — run these on your server:")
    print("─" * 70)
    print(f"\n# 1. Update the token in .env:")
    print(f"sed -i 's|^WYZE_ACCESS_TOKEN=.*|WYZE_ACCESS_TOKEN={access_token}|' {ENV_FILE}")
    print(f"\n# 2. Restart n8n:")
    print(f"cd {COMPOSE_DIR} && docker compose down && docker compose up -d")
    print("\n# Or open .env in nano and replace the WYZE_ACCESS_TOKEN value manually.")
    print("─" * 70)


if __name__ == "__main__":
    auto_push = "--push" in sys.argv

    access_token = get_token()
    print(f"\nNew ACCESS_TOKEN obtained (first 40 chars): {access_token[:40]}...")

    if auto_push:
        pushed = push_to_server(access_token)
        if not pushed:
            print_manual_steps(access_token)
    else:
        print_manual_steps(access_token)
        print("\nTip: Run with --push to have this script SSH and update the server automatically.")
        print("     Requires passwordless SSH access to the server.")
