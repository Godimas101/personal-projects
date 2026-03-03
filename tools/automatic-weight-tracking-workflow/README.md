# Automatic Weight Tracking Workflow

An n8n workflow that automatically reads the latest weight measurement from a Wyze Scale and appends it to [`health-tracking/weight-tracking.md`](../../health-tracking/weight-tracking.md) on GitHub.

The key design challenge: DigitalOcean IPs are blocked from the Wyze login endpoint, so the server can never call `/api/user/login`. This is solved with a **self-refreshing token chain** — you log in once from a residential IP, store both tokens on the server, and `get_wyze_data.py` calls the refresh endpoint (which is NOT IP-blocked) on every run. As long as it runs at least once every 28 days the chain never breaks.

---

## How It Works

```
Schedule Trigger (daily)
  └─ SSH: Execute Wyze Script (get_wyze_data.py on server)
       └─ Parse Python Output
            └─ Process Record (check for new data today)
                 └─ New Data Today?
                      ├─ YES → GitHub Get File → Build Updated File → GitHub Update File
                      └─ NO  → (stop, no commit)
```

1. **Schedule Trigger** — Runs daily at 8 AM
2. **Execute Wyze Script** — SSHes into the server and runs `get_wyze_data.py`
3. **Parse Python Output** — Parses the JSON from stdout
4. **Process Record** — Checks if the reading is from today; extracts weight, body fat, timestamp
5. **New Data Today?** — Skips the commit if no new reading (prevents duplicates)
6. **GitHub Get File → Build Updated File → GitHub Update File** — Fetches the current markdown file, appends a new row, commits it back

---

## Files

| File | Purpose |
|------|---------|
| `get_wyze_data.py` | **Runs on server.** Fetches latest scale record via Wyze SDK. Self-refreshes tokens on every run. |
| `bootstrap-wyze-tokens.py` | **Runs locally.** Break-glass script — logs in from your residential IP and pushes fresh tokens to the server. Only needed if the token chain ever breaks. |
| `credentials.py` | Your local credentials (gitignored — never committed). Created from `credentials.example.py`. |
| `credentials.example.py` | Template showing required fields for `credentials.py`. |
| `wyze-scale-weight-tracker.json` | The n8n workflow JSON — import this into your n8n instance. |
| `patch-workflow.js` | Dev utility for rebuilding the workflow JSON — not needed for normal operation. |

---

## First-Time Setup

### 1. Wyze Prerequisites

- A **native** Wyze account (not Google/Apple SSO — SSO accounts can't use the API)
- Developer API keys from [developer-api-console.wyze.com](https://developer-api-console.wyze.com)
- The Wyze Scale must be owned by (or shared with and accepted on) this API account
- Step on the scale at least once after linking so there's a measurement record

### 2. Local credentials file

```bash
cp credentials.example.py credentials.py
```

Edit `credentials.py` with your real values:

```python
EMAIL    = 'your-wyze-email@example.com'
PASSWORD = 'your-wyze-password'
KEY_ID   = 'your-key-id-from-wyze-developer-portal'
API_KEY  = 'your-api-key-from-wyze-developer-portal'
SERVER   = 'root@your-server.example.com'
```

> `credentials.py` is listed in `.gitignore` and will never be committed.

### 3. Install wyze_sdk locally (one time)

```bash
pip install wyze_sdk
```

### 4. Bootstrap tokens onto the server

Run from your local machine (residential IP required for login):

```bash
python bootstrap-wyze-tokens.py
```

This logs in and prints two `sed` commands. Run them manually in your server terminal:

```bash
sed -i 's|^WYZE_ACCESS_TOKEN=.*|WYZE_ACCESS_TOKEN=<token>|' /root/n8n-docker-caddy/.env
grep -q '^WYZE_REFRESH_TOKEN=' /root/n8n-docker-caddy/.env \
  && sed -i 's|^WYZE_REFRESH_TOKEN=.*|WYZE_REFRESH_TOKEN=<token>|' /root/n8n-docker-caddy/.env \
  || echo 'WYZE_REFRESH_TOKEN=<token>' >> /root/n8n-docker-caddy/.env
```

Or use `--push` to have the script SSH and apply the changes automatically (requires passwordless SSH key configured locally):

```bash
python bootstrap-wyze-tokens.py --push
```

### 5. Add all credentials to server `.env`

Your `/root/n8n-docker-caddy/.env` needs:

```
WYZE_KEY_ID=<your key ID>
WYZE_API_KEY=<your API key>
WYZE_PHONE_ID=n8n-wyze-scale-sync-01ab
WYZE_ACCESS_TOKEN=<from bootstrap step>
WYZE_REFRESH_TOKEN=<from bootstrap step>
GITHUB_PAT=<GitHub personal access token with repo scope>
```

Make sure `WYZE_KEY_ID` and `WYZE_API_KEY` are also in your `docker-compose.yml` environment section so n8n can see them.

### 6. Copy `get_wyze_data.py` to the server

```bash
scp get_wyze_data.py root@your-server:/root/n8n-docker-caddy/
```

Test it manually on the server:

```bash
python3 /root/n8n-docker-caddy/get_wyze_data.py
```

Expected output:
```json
{"data": {"weight": 211.6, "body_fat": 27.2, "bmi": 27.7, "bmr": 1879.0, "muscle": 65.5, ...}}
```

### 7. Import the workflow

Import `wyze-scale-weight-tracker.json` into your n8n instance, configure credentials for the SSH and GitHub nodes, then activate.

---

## Normal Operation

Once set up, nothing needs to be touched. `get_wyze_data.py` calls Wyze's refresh endpoint on every run and writes the new tokens back to `.env` automatically. The rolling 28-day refresh window means the chain stays live indefinitely as long as the workflow runs at least weekly.

### Manual trigger

To log a reading that happened after the scheduled run time, click **Test workflow** in n8n.

---

## Break-Glass: Token Chain Broken

If the server was offline for > 28 days, the refresh token will have expired. Fix it by running `bootstrap-wyze-tokens.py` again from your local machine:

```bash
python bootstrap-wyze-tokens.py --push
```

This does a fresh login from your residential IP (bypassing the datacenter block) and pushes new tokens to the server.

---

## Scale Data Fields

`get_wyze_data.py` returns all available fields from the Wyze `ScaleRecord` object:

| Field | Notes |
|-------|-------|
| `weight` | Already in **lbs** (wyze_sdk handles conversion) |
| `body_fat` | % body fat |
| `bmi` | Body mass index |
| `bmr` | Basal metabolic rate (kcal) |
| `muscle` | Muscle mass (lbs) |
| `body_water` | % body water |
| `bone_mineral` | Bone mineral (lbs) |
| `body_vfr` | Visceral fat rating |
| `protein` | % protein |
| `metabolic_age` | Estimated metabolic age |
| `measure_ts` | Unix timestamp (milliseconds) |
| `timezone` | e.g. `America/Toronto` |
| `mac` | Scale MAC address |
| `user_id` / `family_member_id` | Wyze account user ID |

> **Note:** `body_fat` and other body composition metrics require the scale's impedance measurement — they'll be `null` if the scale only captured weight (e.g. stepped on too quickly, wet feet, etc.)

---

## Architecture Notes

- **Why SSH instead of a direct HTTP call?** Wyze's internal scale API requires HMAC-MD5 signed requests with a hardcoded signing secret. Using the `wyze_sdk` Python library is far simpler and more maintainable than reimplementing the signing in JavaScript inside an n8n Code node.
- **Why not store tokens in n8n credentials?** The tokens need to be updated on every run. Writing back to `.env` and reloading is straightforward; n8n's credential store doesn't support programmatic updates from within a workflow.
- **Weight is already in lbs.** The `wyze_sdk` library converts from the scale's raw kg value before returning. Do not multiply by 2.20462 in the `Process Record` node.
