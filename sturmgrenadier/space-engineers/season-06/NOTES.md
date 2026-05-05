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
- **Plugin listing:** https://torchapi.com/plugins/view/3cd3ba7f-c47c-4efe-8cf1-bd3f618f5b9c (v2.0.5.001, ~24k downloads)
- **⚠ Known issue (still unresolved):** Bot WebSocket dies when the server pauses (no players online) and never auto-reconnects. Plugin reload required. Tried `PauseGameWhenEmpty=false` as a workaround but had to revert (see 2026-05-03 setup log entry — caused boot loop with FSZ). **Plan:** fork the plugin and fix at the source. See "Open Items".

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

### TODO: Build + test the SEDB watchdog fix

**Status:** Code changes done on 2026-05-05. Build + deploy + verify pending for next session.

**Repo:** [Godimas101/sedb-reloaded-again](https://github.com/Godimas101/sedb-reloaded-again)
**Branch:** `feature/decouple-watchdog`
**Commit:** [`e7a3fab`](https://github.com/Godimas101/sedb-reloaded-again/commit/e7a3fab) — "fix: decouple watchdog from status-update feature flag"
**Local checkout:** `c:\Users\Chris Carpenter\VS Code Projects\mods\space-engineers-torch-plugins\sedb-reloaded-again`

**Diagnosis (the actual bug):** The plugin already had auto-reconnect logic in `Timer_Elapsed` (Disconnect+Connect on tick 5, full bridge recreate on tick 24). The timer driving it was started by `InitPost`, but ONLY when `Config.UseStatus = true`. Our `SEDiscordBridge.cfg` has `<UseStatus>false</UseStatus>` (chat-only, no status feature) → timer never starts → watchdog never runs → bot stays dead after gateway drops.

**The fix (3 small changes, 17 insertions / 9 deletions, 2 files):**
1. `SEDiscordBridgePlugin.InitPost` — always `StartTimer()` (was gated on UseStatus).
2. `SEDiscordBridgePlugin.Timer_Elapsed` — gate the status-update block on UseStatus, watchdog above runs unconditionally.
3. `DiscordBridge.RegisterDiscord` — always issue initial `ConnectAsync` (was gated on !UseStatus, meant UseStatus=true servers waited ~25s for first connect via watchdog). Reordered events-before-connect so first Ready event can't be missed.

#### Build env setup (run Setup.bat once, then Visual Studio)

The repo has a `Setup (run before opening solution).bat` that creates two symlinks the .csproj needs to resolve DLL references:
- `GameBinaries` → folder containing `SpaceEngineersDedicated.exe`
- `TorchBinaries` → folder containing `Torch.Server.exe`

We don't run Torch on this machine — server is on GTX. Two options for getting the DLLs:
- **Option A (recommended):** Download Torch separately from [torchapi.com](https://torchapi.com/) and unzip somewhere local. Run Setup.bat pointing at: SE dedicated server (we have one in `D:\SteamLibrary\steamapps\common\SpaceEngineersDedicatedServer\` if installed via Steam tools, otherwise grab the one bundled with the server SDK) and the local Torch folder.
- **Option B (slower):** sFTP the DLLs from the live GTX server into local folders, then point Setup.bat at those.

After symlinks exist, open `SEDiscordBridge.sln` in Visual Studio (or build with `msbuild SEDiscordBridge.sln /p:Configuration=Release`). Output DLL: `SEDiscordBridge\bin\Release\SEDiscordBridge.dll`.

#### Deploy

The custom plugin replaces the official one. On the GTX server's Torch instance:
1. Stop the server.
2. Find the existing SEDiscordBridge plugin (likely `D:\TCAFiles\Users\chrisc8\8269743\Plugins\3cd3ba7f-c47c-4efe-8cf1-bd3f618f5b9c\SEDiscordBridge.dll` — Torch caches plugins under their GUID).
3. Replace that DLL with our built one.
4. Make sure `Torch.cfg` still has `<GetPluginUpdates>false</GetPluginUpdates>` (otherwise Torch will overwrite our DLL with the upstream version on next start). Already false on our server, verified 2026-05-03.
5. Boot.

#### Test plan

1. **Sanity check** — boot, send a message in-game and from Discord. Both directions work? Bot ready? Confirms the build is intact and the fix didn't break the happy path.
2. **The actual regression test** — empty the server for 12+ minutes (server pauses around 10 min idle). Rejoin. Send a chat message in-game. Should appear in `#se-in-game-chat` without a manual `!plugin reload`.
3. **Watch the Torch log** for the timing of the recovery. Expected sequence:
   - `SocketClose Event` (warns when Discord drops the gateway)
   - Several ticks of silent retry counting up
   - One of: a clean `Discord_Zombied → ReconnectAsync()`, OR `Disconnect+Connect` from tick 5 of the watchdog, OR full bridge recreate from tick 24
   - Eventually `Discord Bridge loaded!` again or `Ready` event firing → `Ready=true`
4. **If it doesn't recover** — pull the latest log, look for which path the watchdog took (or didn't take). The most likely regression is that DSharpPlus's `AutoReconnect=true` is somehow racing with our watchdog's manual reconnect. Easy to diagnose from logs.

**Rollback plan:** If the build is broken or the fix regresses, replace our DLL with the original from the upstream `Bishbash777/SEDB-RELOADED` v2.0.5.001 release. We have the GUID-keyed slot in Torch's plugin folder so it's a 1-file swap.

**Long-term:** if this works, open a PR upstream to `Bishbash777/SEDB-RELOADED` so other server admins benefit. Plugin still gets ~24k downloads on torchapi.com.

### Closed: tried PauseGameWhenEmpty=false as a workaround

See 2026-05-03 setup log entry for the post-mortem. Short version: it caused FSZ to spawn safe zones at world load before any player connected, which broke NPC weapon-position state in pre-existing cargo ship / encounter characters and killed the server with a parallel-update NRE 200ms after FSZ initialization. Reverted both PauseGameWhenEmpty and FSZ. SEDB reload-on-demand remains the manual workaround until the fork lands.

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

### 2026-05-03 - Share Inertia Tensor, Solar Radiation (kept). FSZ + PauseGameWhenEmpty (reverted, post-mortem below)
- Enabled `EnableShareInertiaTensor` (was false, now true) across all 3 SE configs — kept
- Enabled solar radiation: `SolarRadiationIntensity` 0 → 5 (LIGHT preset) — kept. Verified preset values via reflection on `Sandbox.Game.dll`: enum `MySolarRadiationIntensity` uses int values DISABLED=0, LIGHT=5, MEDIUM=10, HEAVY=20. Damage mechanics from `Stats.sbc`: 0-100 stat, critical at 74.5 (2 dmg/tick), damage at 100 (10 dmg/tick), decay 0.694/sec when sheltered. Atmospheres still protect.
- Tried disabling `PauseGameWhenEmpty` to fix the SEDB pause-bot-dies issue + added FSZ Faction Safe Zones `1507368483` to compensate for "no idle pause = NPCs grief unattended bases" → **both reverted same day, see post-mortem.**

#### Post-mortem: PauseGameWhenEmpty=false + FSZ deployment failure

**Symptom:** Five consecutive boot attempts after deploy crashed with the same fatal `ParallelTasks.TaskException` wrapping a NRE in `MyCharacterWeaponPositionComponent.Update`. Server never reached "ready" — Torch generated a minidump, Steam auto-restart kicked in, same crash repeated. Took ~6 minutes of crash-loop before the user pulled the plug.

**Diagnosis from logs:** Every single boot attempt followed the same pattern:
```
... [INFO]   Loading session
... [INFO]   Session loaded
... [INFO]   ANTIGRIEF: Got All Safe Zones!     ← FSZ initialization
... 200ms later ...
... [DEBUG]  Exception: NullReferenceException at MyCharacterWeaponPositionComponent.Update
... 200ms later ...
... [FATAL]  ParallelTasks.TaskException → minidump → restart
```

The 200ms gap between "Got All Safe Zones!" and the NRE was suspicious. Then deterministic across 5 boots — that's the smoking gun.

**Root cause:** Combined trigger from BOTH new settings, neither alone:
- `PauseGameWhenEmpty=false` made the world tick from the moment it loaded — before any player connected
- FSZ saw all factions as "offline" (no players logged in), began creating safe zones around faction stations
- Existing NPC characters in the save (cargo ship crew, global encounter NPCs that had previously docked or wandered near faction stations) ended up inside those zones
- The zone-creation flow broke the NPCs' weapon-position component state
- Next parallel character update tick: NRE → fatal exception → crash

The `checkEnemyGrids = true / distanceCheckEnemyGrids = 800m` setting in FSZ should have prevented zone spawning near NPCs, but evidently doesn't catch loose NPC characters or specific NPC types in this codepath.

**Fix:** Reverted both:
- `PauseGameWhenEmpty` true → false → **back to true**
- Removed FSZ ModItem from `Sandbox_config.sbc`

Solar radiation kept (different subsystem, not implicated). Share-inertia kept.

**Lessons:**
1. Never deploy two interacting mods/settings simultaneously when both are untested. Should have deployed `PauseGameWhenEmpty=false` alone first to confirm no bot-stays-alive regressions, THEN added FSZ.
2. SEDB pause-bot-dies bug remains unresolved. Real fix is to fork the plugin and add a watchdog reconnect — see Open Items.
3. FSZ may still be viable in a fresh-world scenario (no legacy NPC clutter near where player factions form). Not retrying on this world.

**Deploy timeline:**
- Initial deploy: commit 40b5770
- Revert: commit 181d19a
- Cleanup pass (this commit): MOTD/README/NOTES tidied
