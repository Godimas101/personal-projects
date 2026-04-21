# BlockLimiter Configuration Reference

Complete reference for configuring the BlockLimiter Torch plugin on our server. Includes pair names, config format, balance strategy, and our current limits.

---

## How BlockLimiter Works

### Core Concepts
- Each `<LimitItem>` is a self-contained rule with a block list, limit count, scope, and punishment
- **Limits stack** — if a block matches multiple LimitItems, ALL must be satisfied (most restrictive wins)
- Setting `LimitGrids` and `LimitPlayers` both true on the same item means the block is denied if EITHER is exceeded
- Config can be hot-reloaded with `!blocklimit reload` — no server restart needed
- Plugin processes 5 grids/second to minimize sim impact
- Blocks aren't deleted by default — they go offline (ShutOffBlock), giving players a chance to fix

### SearchType Options
| Type | Matches | Best for |
|------|---------|----------|
| Auto | TypeId, SubTypeId, AND PairName | General use (default) |
| PairNames | Block pair name only | Grouping vanilla + reskin variants |
| TypeId | Main block category | Umbrella limits (all turrets, all assemblers) |
| SubTypeId | Specific block variant | Individual block targeting |

### GridTypeBlock Filter
| Value | Applies to |
|-------|-----------|
| AllGrids | Everything |
| SmallGridsOnly | Small grids only |
| LargeGridsOnly | Large grids only |
| StationsOnly | Stations only |
| ShipsOnly | Mobile grids only (large + small ships) |

### Punishment Options
| Value | Effect |
|-------|--------|
| None | Warning only |
| ShutOffBlock | Block goes offline (recommended default) |
| DeleteBlock | Block removed |
| Explode | Block explodes |

### Scope Flags
| Flag | Effect |
|------|--------|
| LimitGrids | Count per individual grid |
| LimitPlayers | Count per player across all their grids |
| LimitFaction | Count per faction across all faction grids |

When multiple scope flags are true, block is denied if ANY limit is exceeded.

---

## LimitItem XML Format

```xml
<LimitItem>
  <Name>Human-readable name</Name>
  <BlockList>
    <string>PairNameOrTypeIdOrSubTypeId</string>
    <string>AnotherBlock</string>
  </BlockList>
  <SearchType>PairNames</SearchType>
  <Limit>8</Limit>
  <LimitGrids>true</LimitGrids>
  <LimitPlayers>false</LimitPlayers>
  <LimitFaction>false</LimitFaction>
  <GridTypeBlock>AllGrids</GridTypeBlock>
  <IgnoreNpcs>true</IgnoreNpcs>
  <RestrictProjection>false</RestrictProjection>
  <Punishment>ShutOffBlock</Punishment>
  <Annoy>true</Annoy>
  <Exceptions />
  <LimitFilterType>None</LimitFilterType>
  <LimitFilterOperator>LessThan</LimitFilterOperator>
</LimitItem>
```

---

## Config Patterns

### Pattern 1: Per-Grid Weapon Limit
```xml
<LimitItem>
  <Name>Gatling Turrets (per grid)</Name>
  <BlockList>
    <string>GatlingTurret</string>
    <string>GatlingTurretReskin</string>
  </BlockList>
  <SearchType>PairNames</SearchType>
  <Limit>8</Limit>
  <LimitGrids>true</LimitGrids>
  <LimitPlayers>false</LimitPlayers>
  <IgnoreNpcs>true</IgnoreNpcs>
  <Punishment>ShutOffBlock</Punishment>
  <Annoy>true</Annoy>
</LimitItem>
```

### Pattern 2: Per-Player Limit
```xml
<LimitItem>
  <Name>Gatling Turrets (per player)</Name>
  <BlockList>
    <string>GatlingTurret</string>
    <string>GatlingTurretReskin</string>
  </BlockList>
  <SearchType>PairNames</SearchType>
  <Limit>25</Limit>
  <LimitGrids>false</LimitGrids>
  <LimitPlayers>true</LimitPlayers>
  <IgnoreNpcs>true</IgnoreNpcs>
  <Punishment>ShutOffBlock</Punishment>
  <Annoy>true</Annoy>
</LimitItem>
```

### Pattern 3: Station-Only (Block Ships from Having It)
Set GridTypeBlock to ShipsOnly with Limit 0 — blocks can't be placed on mobile grids.
```xml
<LimitItem>
  <Name>Assemblers (ships blocked)</Name>
  <BlockList>
    <string>Assembler</string>
  </BlockList>
  <SearchType>PairNames</SearchType>
  <Limit>0</Limit>
  <LimitGrids>true</LimitGrids>
  <GridTypeBlock>ShipsOnly</GridTypeBlock>
  <IgnoreNpcs>true</IgnoreNpcs>
  <Punishment>ShutOffBlock</Punishment>
  <Annoy>true</Annoy>
</LimitItem>
```

### Pattern 4: Umbrella "Total Weapons Per Grid"
Use TypeId matching to catch all weapon types under one limit.
```xml
<LimitItem>
  <Name>Total Weapons Per Grid</Name>
  <BlockList>
    <string>LargeGatlingTurret</string>
    <string>LargeMissileTurret</string>
    <string>SmallMissileLauncher</string>
    <string>SmallMissileLauncherReload</string>
    <string>SmallGatlingGun</string>
    <string>InteriorTurret</string>
    <string>ConveyorSorter</string>
  </BlockList>
  <SearchType>TypeId</SearchType>
  <Limit>30</Limit>
  <LimitGrids>true</LimitGrids>
  <IgnoreNpcs>true</IgnoreNpcs>
  <Punishment>ShutOffBlock</Punishment>
  <Annoy>true</Annoy>
</LimitItem>
```
Note: SE weapon TypeIds are unintuitive — gatling turrets are `LargeGatlingTurret`, missile turrets are `LargeMissileTurret`, fixed launchers are `SmallMissileLauncher`, etc. regardless of grid size.

### Pattern 5: Per-Faction Limit
```xml
<LimitItem>
  <Name>Total Turrets Per Faction</Name>
  <BlockList>
    <string>LargeGatlingTurret</string>
    <string>LargeMissileTurret</string>
    <string>InteriorTurret</string>
  </BlockList>
  <SearchType>TypeId</SearchType>
  <Limit>50</Limit>
  <LimitFaction>true</LimitFaction>
  <IgnoreNpcs>true</IgnoreNpcs>
  <Punishment>ShutOffBlock</Punishment>
  <Annoy>true</Annoy>
</LimitItem>
```

---

## Global Config Settings

```xml
<BlockLimiterConfig>
  <EnableLimits>true</EnableLimits>
  <UseVanillaLimits>false</UseVanillaLimits>
  <KillNoOwnerBlocks>false</KillNoOwnerBlocks>
  <MaxBlockSizeShips>15000</MaxBlockSizeShips>
  <MaxBlockSizeStations>0</MaxBlockSizeStations>
  <EnableGridSpawnBlocking>true</EnableGridSpawnBlocking>
  <EnableConvertBlock>true</EnableConvertBlock>
  <BlockOwnershipTransfer>false</BlockOwnershipTransfer>
  <MergerBlocking>true</MergerBlocking>
  <Annoy>true</Annoy>
  <AnnoyInterval>60</AnnoyInterval>
  <AnnoyDuration>15000</AnnoyDuration>
  <PunishInterval>900</PunishInterval>
  <DenyMessage>Limit reached 
{BC} blocks denied 
BlockNames: 
{BL}</DenyMessage>
</BlockLimiterConfig>
```

---

## Player Commands
| Command | Description |
|---------|-------------|
| `!blocklimit mylimit` | Show your current limit violations |
| `!blocklimit limits` | Show all server limit rules |
| `!blocklimit pairnames` | List available pair names |
| `!blocklimit definitions` | List all block definitions |
| `!blocklimit update mylimit` | Refresh your limits (5 min cooldown) |

## Admin Commands
| Command | Description |
|---------|-------------|
| `!blocklimit reload` | Hot-reload config (no restart needed) |
| `!blocklimit enable true/false` | Toggle plugin |
| `!blocklimit violations` | Show all current violations |
| `!blocklimit punish` | Execute punishment on violators |
| `!blocklimit annoy` | Trigger warning to all violators |
| `!blocklimit gridlimit <name>` | Check a grid's limits |
| `!blocklimit playerlimit <name>` | Check a player's limits |
| `!blocklimit factionlimit <tag>` | Check a faction's limits |

---

## Balance Strategy

### Design Goals
1. **Prevent death blobs** — no single grid should be a factory + warship + miner
2. **Force specialization** — combat ships, mining ships, and production bases should be separate
3. **Keep sim speed healthy** — limit the blocks that cause the most server load
4. **Create trade-offs** — players choose between firepower, production, and mobility

### Key Principles (from proven servers)
- **Per-faction turret caps** are the #1 anti-death-blob measure
- **Production on stations only** forces players to build and defend bases
- **Umbrella weapon caps per grid** prevent turret spam even within individual limits
- **Start conservative, loosen later** — easier to relax limits than tighten them
- **ShutOffBlock > DeleteBlock** — gives players a warning, not a loss
- **Annoy messages** warn before punishment — players can self-correct

### Performance Impact Blocks (highest to lowest)
1. Programmable blocks with scripts
2. Active drills and welders
3. Turrets (pathfinding/targeting)
4. Production blocks (assemblers, refineries)
5. Conveyor sorters
6. Projectors

### Sim Speed Thresholds
- 1.0 = healthy
- 0.8 = server struggling
- 0.6 = players will notice lag
- Below 0.5 = unplayable

---

## Block Pair Names

### Weapons — Turrets

| Pair Name | Description |
|-----------|-------------|
| GatlingTurret | Gatling turrets (vanilla) |
| GatlingTurretReskin | Gatling turret reskin (dep mod) |
| MissileTurret | Missile turrets (vanilla) |
| MissileTurretReskin | Missile turret reskin (dep mod) |
| AutoCannonTurret | Autocannon turret |
| LargeCalibreTurret | Artillery turret |
| MediumCalibreTurret | Assault turret |
| InteriorTurret | Interior turret |

### Weapons — Fixed

| Pair Name | Description |
|-----------|-------------|
| GatlingGun | Gatling gun (vanilla) |
| GatlingGunWarfare2 | Gatling gun warfare2 (dep mod) |
| Autocannon | Autocannon (small grid) |
| RocketLauncher | Rocket launcher (large grid) |
| RocketLauncherWarfare2 | Rocket launcher warfare2 (dep mod) |
| SmallRocketLauncherReload | Rocket launcher reload (small grid) |
| LargeCalibreGun | Artillery cannon (fixed) |
| MediumCalibreGun | Assault cannon (fixed) |
| Railgun | Railgun (large + small — may need SubtypeId for different limits) |
| FlareLauncher | Flare launcher (unlimited) |

### Weapons — Modded (Elindis)

Pair names TBD — verify in-game. Use SubtypeId matching:
- `Artillery_MKII` — Artillery MKII turret
- `ElindisGaussTurret` — Gauss turret
- `ElindisTorpedoTurret` — Torpedo turret
- `ElindisHailstormTurret` — Hailstorm turret
- `ElindisTorpedoLauncher` — Torpedo launcher (fixed)

### Ship Tools

| Pair Name | Description | Limit? |
|-----------|-------------|--------|
| Drill | Ship drills | Yes — 10 per grid |
| DrillReskin | Drill reskin (dep mod) | Group with Drill |
| ShipWelder | Ship welders | Yes — 5 per grid |
| ShipWelderReskin | Welder reskin (dep mod) | Group with ShipWelder |
| ShipGrinder | Ship grinders | Yes — 5 per grid |
| ShipGrinderReskin | Grinder reskin (dep mod) | Group with ShipGrinder |
| StaticDrill | ResourceNode drills | NO — do not limit |
| BY_ZWWHDY | Self-Maintenance Unit | Yes — 1/grid, 3/player, static only |

### Production (Station-Only)

| Pair Name | Description |
|-----------|-------------|
| Refinery | Refinery |
| RefineryIndustrial | Industrial refinery (dep mod) |
| Blast Furnace | Basic refinery |
| Assembler | Assembler |
| AssemblerIndustrial | Industrial assembler (dep mod) |
| BasicAssembler | Basic assembler (CANNOT be restricted) |
| OxygenGenerator | H2/O2 generator |
| OxygenGeneratorLab | Lab H2/O2 generator (dep mod) |
| H2 O2 Generator Large | Federal Industrial generator (dep mod) |
| FoodProcessor | Food processor (vanilla) |
| ApexSurvivalAdditionsFoodProcessor | ASA food processor (dep mod) |
| IrrigationSystem | Irrigation system |
| PrototechOrganicAssembler | Prototech organic assembler (ASA) |
| TissueGrowthVat | Tissue growth vat (ASA) |
| AquacultureFarm | Aquaculture farm (ASA) |
| BugFarm | Bug farm (ASA) |
| Apiary | Apiary (ASA) |
| JSLabLarge | Lab large (JS Lab) |
| JSLabEquipment | Lab equipment (JS Lab) |
| JSLargeBlockLabDeskMicroscope | Lab desk microscope (JS Lab) |
| ClangKitchen | Kitchen — 8 pair name variants, list all or use SubtypeId |

### Farming (Station-Only)

| Pair Name | Description |
|-----------|-------------|
| FarmPlot | Vanilla farm plot |
| VertFarmPlot | Vertical farm plot (dep mod) |
| InsetFarmPlot | Inset farm plot (dep mod) |

### Utility / Automation

| Pair Name | Description | Limit? |
|-----------|-------------|--------|
| ProgrammableBlock | Programmable blocks | Yes — 3 per player |
| Projector | Projectors | Yes — 1/grid, 5/player |
| CustomConsoleBlock | Life'Tech console (Projector type) | NO — decorative |
| SurvivalKit | Survival kits | Yes — 1 per grid |
| MedicalRoom | Medical rooms | Yes — static only |
| Wardrobe | Wardrobe (MedicalRoom type) | NO — decorative |
| Kit_Locker | Kit locker (MedicalRoom type) | NO — decorative |
| RefillStation | Refill stations | NO |
| RefillStationInset | Inset refill stations | NO |
| VCZ_Elevator_Buttons | Elevator buttons (MedicalRoom type) | NO |

### Searchlights
Currently unlimited.
| Pair Name | Description |
|-----------|-------------|
| SGSearchlight | SG searchlight (mod) |
| Searchlight | Vanilla searchlight |

---

## Current Limits (from README — to migrate)

### Turrets (per player / per grid)
- Gatling Turret: 25 / 8
- Missile Turret: 15 / 6
- Autocannon Turret: 10 / 6
- Artillery Turret: 5 / 3
- Assault Turret: 10 / 4
- Interior Turret: 40 / 10
- Artillery MKII: 2 / 1
- Gauss Turret: 10 / 4
- Torpedo Turret: 5 / 2
- Hailstorm Turret: 10 / 4

### Fixed Weapons (per player / per grid)
- LG Missile Launcher: 10 / 6
- LG Artillery: 6 / 2
- LG Large Railgun: 2 / 1
- LG Elindis Torpedo Launcher: 5 / 2
- SG Gatling Gun: 20 / 8
- SG Autocannon: 10 / 5
- SG Missile Launcher: 10 / 5
- SG Assault Cannon: 8 / 2
- SG Small Railgun: 8 / 3

### Other Limits
- Programmable Block: 3 per player
- Self-Maintenance Unit: 3 per player, 1 per grid, static only
- Projector: 5 per player, 1 per grid
- Survival Kit: 1 per grid
- Medical Room: static only
- Farm Plot: static only
- Ship Drills: 10 per grid
- Ship Welders: 5 per grid
- Ship Grinders: 5 per grid
- Production blocks: static only

### New Limits to Consider
- **Total weapons per grid** — umbrella cap (e.g. 30 total weapons of any type per grid)
- **Total turrets per faction** — anti-death-blob cap (e.g. 50 turrets across all faction grids)
- **Turret Controller Block** — limit to prevent excessive custom subgrid turrets

---

## Notes
- Reskin pair names (from dep mod 3572467804) must be listed alongside vanilla in BlockList
- Railgun pair name covers BOTH large and small — use SubtypeId for different limits
- Elindis weapons need SubtypeId matching (pair names not confirmed)
- ClangKitchen has 8 variants — list all or use SubtypeId
- `BasicAssembler` cannot be restricted per game engine
- `StaticDrill` (ResourceNodes) and `BY_ZWWHDY` (Self-Maintenance Unit) are ShipWelder/Drill types — exclude from tool limits
- `CustomConsoleBlock`, `Wardrobe`, `Kit_Locker`, `VCZ_Elevator_Buttons` use Projector/MedicalRoom types but are decorative — exclude from functional limits
