# Automatic Weight Tracking Workflow

An n8n workflow that automatically reads the latest weight measurement from a Wyze Scale and appends it to [`health-tracking/weight-tracking.md`](../../health-tracking/weight-tracking.md) on GitHub.

## How It Works

1. **Trigger** — Runs daily at 8 AM (or manually)
2. **Load Tokens** — Reads `WYZE_ACCESS_TOKEN` and `WYZE_USER_ID` from n8n environment variables
3. **Prepare Scale Request** — Signs the API request using HMAC-MD5 (Wyze's internal scale service requires signed requests)
4. **Get Scale Record** — Calls the Wyze scale API (`wyze-scale-service.wyzecam.com`) to fetch the latest reading
5. **Process Record** — Converts weight from kg → lbs, checks if the reading is from today
6. **New Data Today?** — Skips the commit if no new reading exists (prevents duplicate rows)
7. **GitHub Get File** → **Build Updated File** → **GitHub Update File** — Fetches the current markdown file, appends the new row, and commits it back to GitHub

## Files

| File | Purpose |
|------|---------|
| `wyze-scale-weight-tracker.json` | The n8n workflow — import this into your n8n instance |
| `test_wyze_login.py` | One-time script to get initial `WYZE_ACCESS_TOKEN` and `WYZE_USER_ID` from Wyze |
| `refresh-wyze-token.py` | Run this every ~2 days when the access token expires — prints the server update commands |
| `patch-workflow.js` | Utility script used to build/rebuild the workflow JSON — not needed for normal operation |

## Setup

### n8n Environment Variables

Add these to your `.env` and `docker-compose.yml` environment section:

```
WYZE_ACCESS_TOKEN=<from test_wyze_login.py>
WYZE_USER_ID=<from test_wyze_login.py — the user_id field>
WYZE_KEY_ID=<your Wyze developer key ID>
WYZE_API_KEY=<your Wyze developer API key>
WYZE_PHONE_ID=n8n-wyze-scale-sync-01ab
GITHUB_PAT=<GitHub personal access token with repo scope>
```

Get Wyze developer keys at [developer-api-console.wyze.com](https://developer-api-console.wyze.com).

### First-Time Token Setup

```powershell
python test_wyze_login.py
```

Copy the `ACCESS_TOKEN` and `USER_ID` values into `.env`, restart n8n, then import `wyze-scale-weight-tracker.json`.

### Refreshing the Access Token (~every 2 days)

The Wyze access token expires after ~2 days. When the workflow starts failing:

```powershell
python refresh-wyze-token.py
```

This logs in via the Wyze SDK and prints the exact `sed` command to update the token on your server, plus the `docker compose` restart command. Run with `--push` to have it SSH and update the server automatically (requires passwordless SSH access).

## Notes

- The Wyze scale service endpoint requires HMAC-MD5 signed requests — the signing is handled entirely inside the `Prepare Scale Request` Code node using pure JavaScript (no external libraries needed in n8n)
- The workflow checks that the reading is from **today** before logging — stepping on the scale after 8 AM? Run the workflow manually from n8n
- Weight is stored in **lbs** (converted from the raw kg value the scale returns)
- Body fat % is logged if the scale measured it; left blank otherwise
