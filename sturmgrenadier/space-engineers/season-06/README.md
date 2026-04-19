# Sturmgrenadier - Space Engineers Season 06

## Server Info

- **Server Name:** Sturmgrenadier Season 06
- **Host:** GTX Gaming (New York)
- **Slots:** 10
- **Status:** Pre-season (Creative testing)

## Plugins

### Quantum Hangar
Store ships server-side to free up resources.

| Command | Description |
|---------|-------------|
| `!hangar save` | Save the grid you are looking at |
| `!hangar load` | Load a stored grid near you |
| `!hangar list` | View your stored grids |

- **10 hangar slots** per player
- Grid must be **100+ blocks** to hangar
- Mobile grids from inactive players are **auto-hangared after 7 days**
- Stations are not auto-hangared

### Ship Fixer
Fix bugged grids that won't move, stop, or rotate.

| Command | Description |
|---------|-------------|
| `!fixship` | Fix the grid you are looking at |
| `!fixship <name>` | Fix a grid by name (must be owner) |

- **2 minute cooldown** between uses
- Exit all seats before using
- Disconnect connectors and landing gear first

## Server Schedule

- **Auto-save:** Every 5 minutes (via Essentials plugin)
- **Restart:** Every 4 hours with warnings at 15 min, 10 min, and 30 seconds

### On Restart
The following cleanup runs automatically:
- Asteroid voxels reset
- Floating objects deleted
- Projectors disabled
- Welders disabled
- Unowned grids deleted
- Grids under 30 blocks deleted

## Block Restrictions

### Grid & PCU Limits
- **Max grid size:** 15,000 blocks
- **PCU per player:** 50,000

### Utility Blocks

| Block | Per Player | Per Grid | Notes |
|-------|-----------|----------|-------|
| Programmable Block | 3 | - | |
| Self-Maintenance Unit | 3 | 1 | Static grids only |
| Projector | 5 | 1 | Disabled on restart |

### Ship Tools (excludes Resource Nodes and Welder Wall)

| Block | Per Grid | Notes |
|-------|----------|-------|
| Drill | 10 | |
| Welder | 5 | Disabled on restart |
| Grinder | 5 | |

### Production Blocks — Static Grids Only
Refineries, assemblers, and H2/O2 generators can only be placed on stations.

### Weapons — Large Grid Turrets

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

### Weapons — Small Grid Turrets

| Turret | Per Player | Per Grid |
|--------|-----------|----------|
| Gatling Turret | 25 | 8 |
| Missile Turret | 15 | 6 |
| Assault Turret | 10 | 4 |

### Weapons — Large Grid Fixed

| Weapon | Per Player | Per Grid |
|--------|-----------|----------|
| Rocket Launcher | 10 | 6 |
| Artillery | 6 | 2 |
| Large Railgun | 2 | 1 |
| Torpedo Launcher (Elindis) | 5 | 2 |

### Weapons — Small Grid Fixed

| Weapon | Per Player | Per Grid |
|--------|-----------|----------|
| Gatling Gun | 20 | 8 |
| Autocannon | 10 | 5 |
| Rocket Launcher | 10 | 5 |
| Assault Cannon | 8 | 2 |
| Small Railgun | 8 | 3 |

Flare launchers and searchlights are unlimited.

## Mod Collection

[Steam Workshop Collection](https://steamcommunity.com/sharedfiles/filedetails?id=3356806280) (39 mods)
