# Sturmgrenadier Space Engineers - Season 06

## Server Setup

- **Status:** Online (Pre-season Creative testing)
- **Host:** GTX Gaming (gtxgaming.co.uk)
- **Control Panel:** https://gamepanel.gtxgaming.co.uk/Service/Home/8269743
- **Type:** Dedicated Server running Torch API
- **Server Software:** Torch (replaces vanilla `SpaceEngineersDedicated.exe`)

### Tools
- **FTP Client:** WinSCP (sFTP access to GTX server files)
- **Discord Monitoring:** Self-hosted DiscordGSM on OVH VPS (server status alerts via webhook)

### Our Server Specs
| Setting | Value |
|---------|-------|
| Slots | 10 |
| Location | New York |
| CPU | 5.7GHz Ryzen 9 or better (+20% Clock Boost) |
| RAM | Up to 8GB |
| Storage | Up to 100GB NVMe (7500MB/s) |
| CPU Priority | High |

## GTX Gaming

### Plans Available
| Plan | Slots | RAM | Storage | Price |
|------|-------|-----|---------|-------|
| Basic | 10 | 8GB | 100GB NVMe | £8.99/mo |
| Medium | 30 | 12GB | 100GB NVMe | £33.09/mo |
| Large | 60 | 16GB | 100GB NVMe | £61.39/mo |
| Custom | Variable | Variable | Variable | Variable |

### Relevant Locations
- North America: New York, Chicago, Dallas, Quebec, Los Angeles, Miami, Charlotte, Portland
- Europe: London, Paris, Frankfurt, Amsterdam, Stockholm, Helsinki

### Features
- One-click Steam Workshop mod install
- Torch support
- Scheduled restarts, broadcasts, updates, RCON commands
- Automatic daily backups + manual backups + one-click restore
- DDoS protection on all locations
- 24/7 support (chat, tickets, Discord)
- Ryzen 9 7950x/5950x CPUs, DDR5, Windows Server 2022

## Torch API

Torch is a community wrapper for the SE Dedicated Server that adds a WPF GUI, chat integration, entity manager, config editor, and a plugin system.

### Folder Structure (on server)
```
Torch/
├── Torch.Server.exe              <- main executable
├── Torch.cfg                     <- plugin GUIDs listed here
├── Plugins/                      <- plugin .zip files (don't extract)
├── Instance/
│   ├── SpaceEngineers-Dedicated.cfg
│   └── Saves/
└── UserData/                     <- logs, plugin configs
```

### Plugin Installation
1. Get plugin GUID from torchapi.com URL
2. Drop `.zip` in `Plugins/` (do NOT extract)
3. Add GUID to `Torch.cfg` under `<Plugins>`
4. Restart server

## Torch Plugins

### 1. Essentials (`cbfdd6ab-4cda-4544-a201-f73efa3d46c0`)
- **Author:** Bishbash777
- **Version:** v1.7.5.13-9-gfb62249
- **Purpose:** Official utility plugin — adds admin chat commands and server management tools
- **Docs:** https://wiki.torchapi.com/en/Plugins/Essentials

### 2. Quantum Hangar (`24fc7724-0740-4a54-8bb3-1191fd3c8db4`) — REMOVED 2026-04-26
> Functionality is being added to the vanilla game, plugin no longer needed. Section kept for historical reference.

- **Author:** Casimir
- **Version:** v3.2.69
- **Purpose:** Server-side grid storage system — players can save/load ships
- **Features:**
  - `!hangar save` — store the grid you're looking at
  - `!hangar load [Name/ID]` — retrieve a stored grid
  - `!hangar list` — show stored ships and PCU
  - `!hangar sell [Name/ID] [price] [description]` — list for sale
  - Anti-PvP abuse: checks for enemies within configurable distance
  - Cross-server hangar via shared directory
  - Auto dupe/loss prevention on crash
  - Different limits for Normal vs Scripter players
- **Requires:** HangarMarket Mod for buy/sell functionality (not enabled yet — future consideration)

### 3. ALE ShipFixer (`894d12eb-68e1-4eaa-b8c2-263f004629d7`)
- **Author:** LordTylus
- **Version:** v1.0.10.4
- **Purpose:** Fixes bugged/stuck grids that won't move, stop, or rotate
- **How it works:** Cuts and re-pastes the grid to reset physics state
- **Commands:**
  - `!fixship` — fix grid you're looking at
  - `!fixship <name>` — fix by name (must own the grid)
  - `!fixshipmod` / `!fixshipmod <name>` — moderator versions (no cooldown/ownership check)
- **Config:** `ShipFixer.cfg` — cooldown (120s), confirmation timeout (30s)
- **Restrictions:** Fails if connectors/landing gear attached or players in seats
- **Source:** https://github.com/LordTylus/SE-Torch-Plugin-ALE-ShipFixer

### 4. Profiler (`da82de0f-9d2f-4571-af1c-88c7921bc063`)
- **Author:** Torch (official)
- **Version:** v3.1.8432.40000
- **Purpose:** Diagnostic tool for identifying causes of server lag
- **Docs:** https://wiki.torchapi.com/index.php?title=Plugins/Profiler

### 5. SEDiscordBridge (`3cd3ba7f-c47c-4efe-8cf1-bd3f618f5b9c`)
- **Author:** Bishbash777
- **Version:** v2.0.5.001
- **Purpose:** Bridges in-game chat to Discord (chat only — status handled by DiscordGSM)
- **Discord channel:** #se-in-game-chat
- **Config:** `SEDiscordBridge.cfg` — chat-only, no lifecycle/status messages
- **Bot:** Separate bot from DiscordGSM (two bots can't share a token)
- **Note:** Bot needs full member permissions in Discord (not guest) to avoid echo loop
- **Source:** https://github.com/Bishbash777/SEDB-RELOADED
- **⚠ Known issue:** Bot WebSocket dies when the server pauses (no players online) and never auto-reconnects. Plugin reload required. Plugin is also delisted from torchapi.com (likely abandoned). See "Open Items" below for proposed auto-reload solution.

### 6. Multigrid Projector (`d9359ba0-9a69-41c3-971d-eb5170adb97e`)
- **Author:** Viktor
- **Version:** v0.8.7.0
- **Purpose:** Enables building/repairing multi-grid structures (mechs, PDCs, subgrids) from projector blueprints
- **Features:**
  - Weld multi-grid blueprints in survival and creative
  - Assembler integration to queue missing parts
  - Block highlighting for projected components
  - Works in single-player and multiplayer
- **Client requirement:** Players need the Pulsar plugin loader + Multigrid Projector client plugin
  - Install Pulsar: https://github.com/sepluginloader/SpaceEngineersLauncher
  - Open SE → Plugins menu → enable Multigrid Projector → restart game
  - Most welding works even without the client plugin, but full functionality requires it
- **Source:** https://github.com/viktor-ferenczi/se-multigrid-projector

### 7. Performance Improvements (`c2cf3ed2-c6ac-4dbd-ab9a-613a1ef67784`)
- **Author:** Viktor
- **Version:** v1.11.18.0
- **Purpose:** Server-side performance patches for SE
- **Key improvements:**
  - Grid merging ~60-70% faster (disables conveyor updates during merge)
  - Grid pasting optimized (suspends updates while pasting)
  - EOS P2P stats overhead reduced by ~98%
  - Explicit GC.Collect calls removed (eliminates long pauses on load/unload)
  - Safe zone caching (IsSafe results cached for 2 seconds)
  - Wind turbine atmosphere check caching
  - Turret targeting memory allocation optimization
  - Conveyor reachability calculation improvements
  - ~10% lower simulation CPU load from disabling mod API call stats
- **Source:** https://github.com/viktor-ferenczi/se-performance-improvements

## Discord Monitoring

Server status is monitored by a self-hosted instance of [DiscordGSM](https://github.com/DiscordGSM/GameServerMonitor) running on the OVH VPS (`/opt/tcs/discordgsm`). It queries the SE server via A2S protocol every 60 seconds and posts status changes to Discord via webhook.

- **Query port:** 29165 (same as game port)
- **Discord channel:** #se-server-notifications
- **Alerts:** Webhook fires on server online/offline status change

## GTX Knowledge Base

Key articles at `gtxgaming.co.uk/clientarea/index.php?rp=/knowledgebase/101/Space-Engineers`:

- **Torch & Plugins install** — How to Install TORCH and PLUGINS on your Crossplay Space Engineers Dedicated Server
- **Add mods (PC-only)** — How to add mods to your [PC-ONLY] Space Engineers dedicated server
- **Memory/Block Cleanup** — Torch commands for memory and block cleanup via in-game chat
- **Become admin** — How to become ADMIN on your Crossplay PC-CONSOLE Space Engineers dedicated server
- **Auto restarts** — How to setup automatic server restarts
- **Upload world** — How to upload your world from your PC or other provider
- **sFTP access** — How to Connect to Your Dedicated Game Server via sFTP
- **Server files/folders** — How to access your server files and folders
- **Backups** — How to backup / restore / download server backups
- **VRage Remote** — How to connect to VRAGE Remote on your server
- **Server logs** — How to view your server logs
- **Server stats** — How to view your server general statistics

## Mod List

Steam Workshop Collection: https://steamcommunity.com/sharedfiles/filedetails?id=3356806280

**Load order matters — this list is in the correct order. Do not reorder.**

39 mods total:

| # | Mod Name | Workshop ID |
|---|----------|-------------|
| 1 | Sturmgrenadier Core Mod | 2799678177 |
| 2 | Sturmgrenadier Core Survival | 3361326081 |
| 3 | Sturmgrenadier Core Power | 3362282194 |
| 4 | Sturmgrenadier Core Vanilla Combat | 3364273324 |
| 5 | Sturmgrenadier Core Production | 3369236046 |
| 6 | Hubblegum Skybox | 2645964353 |
| 7 | Say No To Scrap | 1146278097 |
| 8 | Jargon Generator (Mod) | 2470184482 |
| 9 | Sci Fi Button Images | 2324191331 |
| 10 | AQD - LCD Image Extension | 1645942623 |
| 11 | AQD - Concrete | 2298956701 |
| 12 | Emissive Letters & Symbols | 3347016415 |
| 13 | Improvised Experimentation | 2891367014 |
| 14 | Advanced Welding | 510790477 |
| 15 | Stone Yield Nerf | 2370668905 |
| 16 | TBH - Heavier Containers | 2830050106 |
| 17 | TBH - Heavier Tanks | 2936628930 |
| 18 | Braced Conveyor Pipe | 2806327649 |
| 19 | EDP - Thruster Covers | 3383813378 |
| 20 | Slope LCD Panels Redux | 2206564401 |
| 21 | Grated Catwalks Expansion | 2503712170 |
| 22 | Rebels Lights 1.2.01 | 2718175525 |
| 23 | Aryx-Lynxon Drive Systems | 2394430829 |
| 24 | Self-Maintenance Unit | 3515485609 |
| 25 | AQD - Upgradeable Gyroscopes | 2621169600 |
| 26 | AQD - Armor Expansion | 1939935505 |
| 27 | ResourceNodes | 2493091475 |
| 28 | Tank Tracks Framework & API | 3208995513 |
| 29 | Tank Tracks Builder | 3209005014 |
| 30 | Tank Tracks over Vanilla Wheels | 3209008231 |
| 31 | AQD - Conveyor Expansion | 1864380341 |
| 32 | Blast Door Sections Retextured | 1574837911 |
| 33 | Rotary Airlock | 1359954841 |
| 34 | WelderWall | 3370792625 |
| 35 | Neon tubes + | 3373230204 |
| 36 | VCZ Elevator v2.0 | 3030780799 |
| 37 | Faux Ship Lights | 637514816 |
| 38 | ARC Truss System | 3701176691 |
| 39 | TSO - More Corridor Blocks | 3611423853 |
| 40 | Tank Track Overlay (Variant) | 3225398014 |
| 41 | Zkillerproxy Client | 1469072169 |
| 42 | Compressed Ores | 2825470671 |

## Directory Layout

- `config/` — Local copies of server configuration files
- `NOTES.md` — This file; setup notes and decisions

## Open Items

### TODO: Auto-reload SEDiscordBridge after a player joins

**Symptom:** Discord chat bridge stops working in both directions after the server has been empty for a while. Players joining later find their chat doesn't reach Discord, and Discord messages don't reach the game. Only fix that's worked so far is restarting Torch.

**Root cause** (confirmed via Torch log analysis on 2026-04-28):
- Server pauses when no players online (default SE behavior).
- Paused main thread blocks DSharpPlus's WebSocket heartbeat to Discord.
- Discord drops the gateway connection (`SocketClose Event` warning in Torch log).
- The plugin's auto-reconnect logic doesn't recover. Bot stays dead until plugin is reloaded.
- Pattern observed multiple times in one day: each `SocketClose Event` was the last SEDiscordBridge entry until a server restart.

**Plan:** Add an Essentials AutoCommand that runs `!plugin reload SEDiscordBridge` when a player joins the server. Server resumes on player connect, so this is the natural moment to revive the bot.

**Approach 1 — Player-join trigger (preferred):**
```xml
<AutoCommand>
  <Enabled>true</Enabled>
  <CommandTrigger>Connect</CommandTrigger>
  <Name>ReloadSEDBOnJoin</Name>
  <OnStart>false</OnStart>
  <DayOfWeek>All</DayOfWeek>
  <Steps>
    <CommandStep>
      <Delay>00:00:10</Delay>
      <Command>!plugin reload SEDiscordBridge</Command>
    </CommandStep>
  </Steps>
</AutoCommand>
```
The 10-second delay lets the server fully wake and the player finish connecting before the reload fires.

**Approach 2 — Periodic reload (fallback if Approach 1 doesn't work):**
A `Timed` AutoCommand running `!plugin reload SEDiscordBridge` every 30 minutes. Works regardless of trigger support, costs almost nothing, but adds a worst-case 30-min lag before a dead bot recovers.

**To verify before / after deploying:**
1. Confirm Essentials in this build supports `Connect` as a CommandTrigger. If not, try `Join`. If neither works (server logs `Unknown command trigger: ...` at startup), fall back to Approach 2.
2. Confirm the Torch reload command is `!plugin reload <Name>` vs `!plugins reload` vs the GUID form. Test from Torch console.
3. After deployment: disconnect everyone, wait for server to pause, reconnect, watch Torch log for `Server is running command '!plugin reload SEDiscordBridge'` — this confirms the trigger fires correctly.

**Caveat:** First player's join announcement may not reach Discord because the bot is mid-reload during their connect. Acceptable trade-off vs total chat outage.

**Long-term:** SEDiscordBridge is delisted from torchapi.com (author appears to have abandoned it). Once a chat-bridge replacement is identified or a working fork is found, this auto-reload workaround can be removed.

## Setup Log

### 2026-04-18 - Initial setup & research
- Created project directory and folder structure
- Researched GTX Gaming hosting plans and features
- Documented Torch API setup and folder structure
- Configured all Torch plugins: Essentials, Quantum Hangar, ALE ShipFixer, Profiler
- Set up Essentials AutoCommands: auto-save (5 min), scheduled restart (4 hr), vote restart
- Configured server settings: Creative mode, 10x inventory, PER_PLAYER PCU (50k), 15k block grid cap
- Set up Steam group whitelist, admin access, MOTD with plugin info
- Configured Block Restrictions mod: weapons, tools, production, utility block limits
- Created AdditionalItems.ini for InfoLCD modded item support

### 2026-04-20 - Discord monitoring & polish
- Tried SEDiscordBridge — removed due to startup race condition (bot connects after "Started" event)
- Deployed self-hosted DiscordGSM on OVH VPS via Docker
- Server status alerts working via Discord webhook
- Added Multigrid Projector and Performance Improvements plugins
- Various config tweaks: weather damage, meteors, experimental mode, private mode
- Updated README with Patreon, More Engineer Characters, Multigrid Projector client setup

### 2026-04-26 - Mod additions, Quantum Hangar retired
- Removed Quantum Hangar plugin (functionality being added to vanilla game)
- Deleted `config/torch/QuantumHangar.cfg`
- Added Tank Track Overlay (Variant) `3225398014` (#40) and Zkillerproxy Client `1469072169` (#41) to mod list

### 2026-04-28 - Inventory tuning + Compressed Ores
- Inventory multiplier reduced from 10x to 6x (both Sandbox_config.sbc and SpaceEngineers-Dedicated.cfg)
- Added Compressed Ores `2825470671` (#42) — adds compressed ore items/blueprints to make the lower inventory cap more workable for cargo logistics
- Added block limits for Compressed Ores production blocks:
  - Ore Mill: 4 per player, station only (matches refinery cap; LG only by SBC)
  - Ore Compactors: 8 per player TOTAL across both LG + SG variants, any grid
- Limits applied in both BlockLimiter Torch plugin and BlockRestrictions mod (belt-and-suspenders)
