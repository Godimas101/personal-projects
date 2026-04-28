<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&height=170&color=0:06121E,45:0F766E,100:2563EB&text=⚔️%20Sturmgrenadier%20Season%2006&fontColor=ffffff&fontAlignY=35&fontSize=30&desc=Space%20Engineers%20Dedicated%20Server&descAlignY=57&descSize=18" />
</p>

> **"Ten engineers, one star system, and a suspicious number of turrets."**

## 🖥️ Server Info

- **Server Name:** Sturmgrenadier Season 06
- **IP Address:** `64.20.48.139:29165`
- **Max grid size:** 15,000 blocks
- **PCU per player:** 50,000
- **Max Players:** 10
- **Access:** Private — you must be a member of the [SG Space Engineers Whitelist](https://steamcommunity.com/groups/SGSPE) Steam group to connect
- **Status:** Pre-season (Creative testing)
- **Server Status:** <a href="https://discord.com/channels/257714976125353985/1495906930068291717">📣 #se-server-status</a> on Discord
- **Notifications:** <a href="https://discord.com/channels/257714976125353985/1495824736696012840">📣 #se-server-notifications</a> on Discord
- **In-Game Chat:** <a href="https://discord.com/channels/257714976125353985/1495907300387455090">💬 #se-in-game-chat</a> on Discord
- **Host:** GTX Gaming (New York) — [Control Panel](https://gamepanel.gtxgaming.co.uk/Service/Home/8269743) (admin only)

## 🧡 Support the Server

Server costs are covered by community contributions. The more subscribers we have, the more powerful our hardware gets. Not mandatory — but if you're having fun, consider chipping in.

[![Support on Patreon](https://raw.githubusercontent.com/Godimas101/personal-projects/main/patreon/images/buttons/patreon-medium.png)](https://patreon.com/Godimas101)

## ⏰ Server Schedule

- **Auto-save:** Every 5 minutes
- **Restart:** Every 4 hours with warnings at 15 min, 10 min, and 30 seconds

### 🧹 On Restart
The following cleanup runs automatically:
- Asteroid voxels reset
- Floating objects deleted
- Projectors disabled
- Welders disabled
- Unowned grids deleted
- Grids under 30 blocks deleted

---

<p align="center"><img src="../images/readme/torch.png" height="200" /></p>

## 🔌 Torch Plugin Info

### 🔧 Ship Fixer
Fix bugged grids that won't move, stop, or rotate. The engineering equivalent of "turn it off and on again."

| Command | Description |
|---------|-------------|
| `!fixship` | Fix the grid you are looking at |
| `!fixship <name>` | Fix a grid by name (must be owner) |

- **2 minute cooldown** between uses
- Exit all seats before using
- Disconnect connectors and landing gear first

### 🗳️ Vote Restart
Think the server needs a reboot before the next scheduled restart? Call a vote.

| Command | Description |
|---------|-------------|
| `!vote VoteRestart` | Start a restart vote |

- Needs **50% of online players** to pass
- Runs the full cleanup sequence before restarting

### 💬 Discord Integration
- **Server status** (online/offline) monitored in `#se-server-notifications` via DiscordGSM
- **In-game chat** bridged to `#se-in-game-chat` — talk to players from Discord and vice versa

### 🧩 Multigrid Projector
Build and weld multi-grid blueprints (mechs, subgrid turrets, etc.) from a single projector.

**Client setup required for full functionality:**
1. Install **Pulsar** (SE plugin loader): [github.com/sepluginloader/SpaceEngineersLauncher](https://github.com/sepluginloader/SpaceEngineersLauncher)
2. Launch Space Engineers
3. Go to **Plugins** menu → enable **Multigrid Projector**
4. Restart the game

Most multi-grid welding works without the client plugin, but assembler integration and block highlighting require it.

### ⚡ Performance Improvements
Server-side performance patches — faster grid merging, safe zone caching, reduced CPU overhead, and more. No player action needed.

### 🚧 Block Limits

Managed by the [BlockLimiter](https://torchapi.com/plugins/view/11fca5c4-01b6-4fc3-a215-602e2325be2b) Torch plugin. Blocks over the limit are shut off. Use `!blocklimit mylimit` in chat to check your status.

#### 💥 Total Weapons Per Grid
Includes all turrets (except interior), fixed weapons, and turret controllers.

| Grid Type | Max Weapons |
|-----------|------------|
| Stations | 18 |
| Large Ships | 8 |
| Small Ships | 10 |

#### 🔫 Turrets (per player / per grid)

| Turret | Per Player | Per Grid |
|--------|-----------|----------|
| Gatling Turret | 25 | 8 |
| Missile Turret | 15 | 6 |
| Autocannon Turret | 10 | 6 |
| Artillery Turret | 5 | 3 |
| Assault Turret | 10 | 4 |
| Interior Turret | 40 | 10 |
| Artillery MKII | 2 | 1 |
| Gauss Turret (Elindis) | 10 | 4 |
| Torpedo Turret (Elindis) | 5 | 2 |
| Hailstorm Turret (Elindis) | 10 | 4 |

#### 🎯 Fixed Weapons (per player / per grid)

| Weapon | Per Player | Per Grid |
|--------|-----------|----------|
| Rocket Launcher (LG) | 10 | 6 |
| Artillery (LG) | 6 | 2 |
| Large Railgun | 2 | 1 |
| Torpedo Launcher (Elindis) | 5 | 2 |
| Gatling Gun (SG) | 20 | 8 |
| Autocannon (SG) | 10 | 5 |
| Rocket Launcher (SG) | 10 | 5 |
| Assault Cannon (SG) | 8 | 2 |
| Small Railgun | 8 | 3 |

Flare launchers and searchlights are unlimited.

#### ⛏️ Ship Tools — Ships Only
Ship tools cannot be placed on stations. Use Welder Walls and Resource Nodes instead. Capped per player (across all your grids) — share a mining ship or specialize your fleet.

| Tool | Per Player |
|------|-----------|
| Drill | 10 |
| Welder | 5 |
| Grinder | 5 |

#### 🏗️ Static Grid Tools

| Block | Per Player | Per Grid | Notes |
|-------|-----------|----------|-------|
| Welder Wall | 60 | — | Static only |
| Resource Nodes | 10 | — | Static only |
| Self-Maintenance Unit | 3 | 1 | Static only |
| Ganymede Incinerator | — | 1 | Any grid |

Prototech Drills are salvage items — no limits.

#### 🏭 Production — Static Grids Only
Build your factory, then fly to it.

| Block | Per Player | Notes |
|-------|-----------|-------|
| Refinery + Industrial | 4 | |
| Blast Furnace | 6 | |
| x10 Refinery | 1 | |
| Ore Mill | 4 | LG only |
| Ore Compactor | 8 | LG + SG combined, any grid |
| Assembler + Industrial | 4 | |
| Basic Assembler | 5 | |
| H2/O2 Generator | 12 | |
| Food Processor / Kitchen | 4 | Any grid allowed |
| Prototech Organic Assembler | 2 | |
| Tissue Growth Vat | 4 | |
| Aquaculture Farm | 4 | |
| Bug Farm | 4 | |
| Apiary | 6 | |
| JS Labs | 4 | Any grid allowed |

Prototech Refinery and Prototech Assembler are salvage items — no limits, but assembler is static only.

#### 🌱 Farming

| Block | Per Player | Per Grid | Notes |
|-------|-----------|----------|-------|
| Farm Plot (all variants) | 30 | 12 station / 4 ship | |
| Oxygen Farm | — | 10 | Any grid |
| Algae Farm | 6 | — | Any grid |
| Irrigation System | 10 | 2 per station | |

#### 🛠️ Utility Blocks

| Block | Per Player | Per Grid | Notes |
|-------|-----------|----------|-------|
| Programmable Block | 3 | — | |
| Projector | 5 | 1 | Disabled on restart |
| Survival Kit | — | 1 | |
| Medical Room | — | — | Static only |
| AI Blocks (combined) | 30 | — | Basic / Flight / Offensive / Defensive / Recorder — for drones + player-made weapons |
| Event Controller | 30 | 5 | Performance-sensitive, keep counts reasonable |

#### ⚙️ Performance-Sensitive Blocks

These cap the blocks most likely to hurt sim speed. Be reasonable — the server runs better for everyone.

| Block | Per Player | Per Grid | Notes |
|-------|-----------|----------|-------|
| Conveyor Sorter | 100 | 20 | Routing pathfinding scales with count |
| Mechanical Blocks (combined) | 50 | — | Rotors + pistons + hinges; subgrid physics is expensive, spend them how you like |
| Safe Zone | 1 | — | Each active zone burns sim time |
| Sensor | — | 10 | Periodic raycasts |
| Gravity Generator | — | 5 | Flat + sphere combined |
| Jump Drive | — | 3 | |

---

<p align="center"><img src="../images/readme/steam-workshop.png" height="200" /></p>

## 🧱 Mod Info

### 👤 [More Engineer Characters](https://steamcommunity.com/sharedfiles/filedetails/?id=2028943594)

Choose your suit at any medical room. Each has different strengths and trade-offs.

| Suit | Strengths | Weaknesses |
|------|-----------|------------|
| **Fighter** | 2x health | Severely limited inventory |
| **Builder** | 2x inventory capacity | Reduced jetpack efficiency |
| **Explorer** | Better temperature tolerance, more hydrogen | Jetpack mainly works in space |
| **NextGen** | Balanced — fighter durability + extra storage | Jack of all trades |

### 📺 [HudLcd](https://steamcommunity.com/workshop/filedetails?id=911144486)

Display LCD text directly on your HUD while piloting. Add `hudlcd` to an LCD panel's custom data to activate.

**Syntax:** `hudlcd:{PosX}:{PosY}:{FontSize}:{Colour}:{Shadow}`

Coordinates are screen-relative: `0:0` is center, `-1:-1` is bottom-left, `1:1` is top-right. Leave parameters blank for defaults.

| Example | Effect |
|---------|--------|
| `hudlcd:-1:1` | Top-left corner |
| `hudlcd:-0.35:-0.65` | Above hotbar |
| `hudlcd:::0.5` | Half font size, default position |
| `hudlcd::::red:1` | Red text with shadow |

FontSize is a multiplier (1 = normal, 0.5 = half, 2 = double). Colour accepts names (`red`), RGB (`255,0,0`), or RGBA. Set Shadow to `1` to enable.

### 🔍 [Build Info](https://steamcommunity.com/workshop/filedetails?id=514062285)

Shows detailed block stats (mass, integrity, power draw, inventory capacity) when holding or aiming at blocks. Open settings with chat → F2.

**Key commands:**

| Command | What it does |
|---------|-------------|
| `/bi help` | Full feature list and hotkey reference |
| `/bi conveyorvis` | Visualize conveyor networks — color-coded lines, red = unconnected, pink = cross-grid |
| `/bi worldinfo` | Show world settings and active mods |
| `/bi shipmods` | Show DLCs and mods used by the targeted ship |
| `/bi reload` | Reload config mid-game |

**Overlay hotkeys:**

| Key | Action |
|-----|--------|
| Ctrl + Plus | Cycle through overlays (mount points, conveyor ports, airtightness) |
| Shift + R | Lock overlay to aimed block |
| Alt + R | View construction stage models |
| Ctrl + R | Grab aimed block to toolbar |

[Full command reference](https://gist.github.com/THDigi/4c59566005d0e1255ead543fdb90f16d)

### 🔧 [AQD - Easy Tool Access](https://steamcommunity.com/workshop/filedetails?id=3707426899)

Quick-switch between tools and weapons from a single hotbar slot. Hold the assigned hotbar key to open the tool wheel, mouse over your choice, release to equip. Customize bindings via F2 menu.

### 🧪 [Improvised Experimentation](https://steamcommunity.com/sharedfiles/filedetails?id=2891367014)

Grab, carry, rotate, and throw grids by hand. Works in singleplayer and on dedicated servers. Type `/IME` in chat for settings.

| Action | Key |
|--------|-----|
| Grab / Drop | R |
| Rotation Mode | LMB (hold or toggle) |
| Change Grab Point | RMB (hit point vs center of mass) |
| Throw | LMB + RMB held |
| Adjust Distance | Scroll wheel |
| Set Reference Grid | MMB |
| Toggle Alignment | Shift (camera vs grid) |
| Cycle Facing | Alt |
| Cycle Up Face | Ctrl |

### 🔩 [Advanced Welding](https://steamcommunity.com/sharedfiles/filedetails?id=510790477)

Three features in one:
- **Weld Pads** — ultra-slim single-use merge blocks, great for subgrid builds
- **Detach Mode** — hold Ctrl while grinding to cleanly detach a block without losing components
- **Precision Grind** — hold secondary action to focus grinder on a single block

## 📦 Mod Collection

[Steam Workshop Collection](https://steamcommunity.com/sharedfiles/filedetails?id=3356806280) (42 mods)

---

<p align="center"><img src="../images/readme/space-engineers.png" height="200" /></p>
