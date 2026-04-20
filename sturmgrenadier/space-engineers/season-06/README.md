<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&height=170&color=0:06121E,45:0F766E,100:2563EB&text=⚔️%20Sturmgrenadier%20Season%2006&fontColor=ffffff&fontAlignY=35&fontSize=30&desc=Space%20Engineers%20Dedicated%20Server&descAlignY=57&descSize=18" />
</p>

> **"Ten engineers, one star system, and a suspicious number of turrets."**

## 🖥️ Server Info

- **Server Name:** Sturmgrenadier Season 06
- **Connect:** `64.20.48.139:29165`
- **Host:** GTX Gaming (New York)
- **Slots:** 10
- **Access:** Private — you must be a member of the [SG Space Engineers Whitelist](https://steamcommunity.com/groups/SGSPE) Steam group to connect
- **Status:** Pre-season (Creative testing)
- **Max grid size:** 15,000 blocks
- **PCU per player:** 50,000

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

## 🔌 Torch Plugin Info

### 📦 Quantum Hangar
Store ships server-side to free up resources. Out of sight, out of sim.

| Command | Description |
|---------|-------------|
| `!hangar save` | Save the grid you are looking at |
| `!hangar load` | Load a stored grid near you |
| `!hangar list` | View your stored grids |

- **10 hangar slots** per player
- Grid must be **100+ blocks** to hangar
- Mobile grids from inactive players are **auto-hangared after 7 days**
- Stations are not auto-hangared

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

### 💬 Discord Bridge
Server chat, restart notifications, and sim speed warnings are relayed to Discord via SEDiscordBridge.

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

---

## 🧱 Mod Info

### 🚧 Block Restrictions

#### 🛠️ Utility Blocks

| Block | Per Player | Per Grid | Notes |
|-------|-----------|----------|-------|
| Programmable Block | 3 | — | |
| Self-Maintenance Unit | 3 | 1 | Static grids only |
| Projector | 5 | 1 | Disabled on restart |
| Survival Kit | — | 1 | |
| Medical Room | — | — | Static grids only |
| Farm Plot | — | — | Static grids only |

#### ⛏️ Ship Tools
Excludes Resource Node drills and Welder Wall blocks — those are unlimited on stations.

| Block | Per Grid | Notes |
|-------|----------|-------|
| Drill | 10 | |
| Welder | 5 | Disabled on restart |
| Grinder | 5 | |

#### 🏭 Production Blocks — Static Grids Only
Refineries, assemblers, and H2/O2 generators can only be placed on stations. You build your factory, then you fly to it.

#### 🔫 Weapons — Large Grid Turrets

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

#### 🔫 Weapons — Small Grid Turrets

| Turret | Per Player | Per Grid |
|--------|-----------|----------|
| Gatling Turret | 25 | 8 |
| Missile Turret | 15 | 6 |
| Assault Turret | 10 | 4 |

#### 🎯 Weapons — Large Grid Fixed

| Weapon | Per Player | Per Grid |
|--------|-----------|----------|
| Rocket Launcher | 10 | 6 |
| Artillery | 6 | 2 |
| Large Railgun | 2 | 1 |
| Torpedo Launcher (Elindis) | 5 | 2 |

#### 🎯 Weapons — Small Grid Fixed

| Weapon | Per Player | Per Grid |
|--------|-----------|----------|
| Gatling Gun | 20 | 8 |
| Autocannon | 10 | 5 |
| Rocket Launcher | 10 | 5 |
| Assault Cannon | 8 | 2 |
| Small Railgun | 8 | 3 |

Flare launchers and searchlights are unlimited. Light 'em up.

## 📦 Mod Collection

[Steam Workshop Collection](https://steamcommunity.com/sharedfiles/filedetails?id=3356806280) (39 mods)

*May your sim speed stay above 0.9 and your Clang encounters stay below 1.*
