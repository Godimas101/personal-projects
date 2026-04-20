# Sturmgrenadier Space Engineers - Season 06

## Server Setup

- **Status:** In progress
- **Host:** GTX Gaming (gtxgaming.co.uk)
- **Type:** Dedicated Server running Torch API
- **Server Software:** Torch (replaces vanilla `SpaceEngineersDedicated.exe`)

### Tools
- **FTP Client:** WinSCP (sFTP access to GTX server files)

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

### 2. Quantum Hangar (`24fc7724-0740-4a54-8bb3-1191fd3c8db4`)
- **Author:** Casimir
- **Version:** v3.2.69
- **Purpose:** Server-side grid storage system — players can save/load/trade ships
- **Features:**
  - `!hangar save` — store the grid you're looking at
  - `!hangar load [Name/ID]` — retrieve a stored grid
  - `!hangar list` — show stored ships and PCU
  - `!hangar sell [Name/ID] [price] [description]` — list for sale
  - Anti-PvP abuse: checks for enemies within configurable distance
  - Cross-server hangar via shared directory
  - Auto dupe/loss prevention on crash
  - Different limits for Normal vs Scripter players
- **Requires:** HangarMarket Mod for buy/sell functionality

### 3. ALE ShipFixer (`894d12eb-68e1-4eaa-b8c2-263f004629d7`)
- **Author:** LordTylus
- **Version:** v1.0.10.4
- **Purpose:** Fixes bugged/stuck grids that won't move, stop, or rotate
- **How it works:** Cuts and re-pastes the grid to reset physics state
- **Commands:**
  - `!fixship` — fix grid you're looking at
  - `!fixship <name>` — fix by name (must own the grid)
  - `!fixshipmod` / `!fixshipmod <name>` — moderator versions (no cooldown/ownership check)
- **Config:** `ShipFixer.cfg` — cooldown (default 900s), confirmation timeout (30s)
- **Restrictions:** Fails if connectors/landing gear attached or players in seats
- **Source:** https://github.com/LordTylus/SE-Torch-Plugin-ALE-ShipFixer

### 4. Profiler (`da82de0f-9d2f-4571-af1c-88c7921bc063`)
- **Author:** Torch (official)
- **Version:** v3.1.8432.40000
- **Purpose:** Diagnostic tool for identifying causes of server lag
- **Docs:** https://wiki.torchapi.com/index.php?title=Plugins/Profiler

### ~~5. SEDiscordBridge~~ — REMOVED
- **Reason:** Server startup message race condition — bot connects after the "Started" event fires, so the "Server Online" notification never reaches Discord. Replaced with DiscordGSM external monitoring.

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

### ~~8. ALE Restart Watchdog~~ — REMOVED
- **Reason:** Incompatible with managed hosting (GTX). Could restart the server process but leave the admin panel unable to see it due to port conflicts. GTX has its own scheduled restart feature instead.

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
| 6 | Block Restrictions | 2053202808 |
| 7 | Hubblegum Skybox | 2645964353 |
| 8 | Say No To Scrap | 1146278097 |
| 9 | Jargon Generator (Mod) | 2470184482 |
| 10 | Sci Fi Button Images | 2324191331 |
| 11 | AQD - LCD Image Extension | 1645942623 |
| 12 | AQD - Concrete | 2298956701 |
| 13 | Emissive Letters & Symbols | 3347016415 |
| 14 | Improvised Experimentation | 2891367014 |
| 15 | Advanced Welding | 510790477 |
| 16 | Stone Yield Nerf | 2370668905 |
| 17 | TBH - Heavier Containers | 2830050106 |
| 18 | TBH - Heavier Tanks | 2936628930 |
| 19 | Braced Conveyor Pipe | 2806327649 |
| 20 | EDP - Thruster Covers | 3383813378 |
| 21 | Slope LCD Panels Redux | 2206564401 |
| 22 | Life'Tech Transparent LCD Variants | 3292090990 |
| 23 | Grated Catwalks Expansion | 2503712170 |
| 24 | Rebels Lights 1.2.01 | 2718175525 |
| 25 | Aryx-Lynxon Drive Systems | 2394430829 |
| 26 | Self-Maintenance Unit | 3515485609 |
| 27 | AQD - Upgradeable Gyroscopes | 2621169600 |
| 28 | AQD - Armor Expansion | 1939935505 |
| 29 | ResourceNodes | 2493091475 |
| 30 | Tank Tracks Framework & API | 3208995513 |
| 31 | Tank Tracks Builder | 3209005014 |
| 32 | Tank Tracks over Vanilla Wheels | 3209008231 |
| 33 | AQD - Conveyor Expansion | 1864380341 |
| 34 | Blast Door Sections Retextured | 1574837911 |
| 35 | Rotary Airlock | 1359954841 |
| 36 | WelderWall | 3370792625 |
| 37 | Neon tubes + | 3373230204 |
| 38 | VCZ Elevator v2.0 | 3030780799 |
| 39 | Faux Ship Lights | 637514816 |

## Open Questions

- [ ] World settings (map, mods, game rules)?
- [ ] HangarMarket Mod — do we want the marketplace feature for Quantum Hangar?

## Directory Layout

- `config/` — Local copies of server configuration files
- `NOTES.md` — This file; setup notes and decisions

## Setup Log

### 2026-04-18 - Research & planning
- Researched GTX Gaming hosting plans and features
- Documented Torch API setup and folder structure
- Documented all 4 Torch plugins: Essentials, Quantum Hangar, ALE ShipFixer, ALE Restart Watchdog
- Flagged potential Restart Watchdog compatibility issue with managed hosting

### 2026-04-18 - Initial setup
- Created project directory and folder structure
