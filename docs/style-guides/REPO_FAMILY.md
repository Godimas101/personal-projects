# Repo Family Reference

This file is the **source of truth** for which `capsule-render` header family belongs to each repo.

When a new repo is created, renamed, split out, or rebranded, **update this file at the same time** as its `README.md`.

**Last updated:** 2026-07-14 — mod-docs batch completed (gitpush-mod/.github + Godimas101/.github + TCS org profile rewrite + all 10 mod README rewrites + automation workflows).

---

## Core Rule

- Every public repo should belong to a defined README family.
- The family determines the default `capsule-render` header style for that repo's main `README.md`.
- If a repo needs an exception, document it here so future updates stay consistent.

---

## Family Summary

| Family | Default capsule type | Palette mood | Notes |
|---|---|---|---|
| Space Engineers mods | `waving` | Industrial / spacey blues | All SE mods under `gitpush-mod` |
| MechWarrior 5 mods | `waving` | Steel gray + combat orange | All MW5 mods under `gitpush-mod` — same capsule type as SE, distinct palette |
| SE tools + toolkits | `waving` | Industrial / spacey (matches SE mods) | Standalone SE utilities and tool repos |
| The Canadian Space | `rect` | Dark space + per-repo accent, `textBg=true` | TCS platform repos |
| Utility tools | `slice` | Neutral, tool-forward | Standalone utility apps (non-game) |
| Personal / reference | `venom` | Cool + moody | Personal index/docs repos and reference collections |
| Org profile | `blur` | Family-appropriate | Special `<org>/.github` profile pages |
| GitHub profile (personal) | `blur` header + `soft` footer | Personal brand | Chris's personal profile README (`Godimas101/Godimas101`) |

---

## Current Repo Assignments

### 🎮 Space Engineers mods — `gitpush-mod` org

Palette: spacey/industrial (deep blues, steel, gold-orange accents).

| Repo | Capsule header | Notes |
|---|---|---|
| `gitpush-mod/se-infolcd-apex-update` | `waving` | Flagship: InfoLCD for Apex LCD blocks. 1,335+ subs. Client-side only. |
| `gitpush-mod/se-infolcd-apex-advanced` | `waving` | Sibling variant of InfoLCD. Keep visually consistent with Apex Update. |
| `gitpush-mod/se-not-just-for-looks` | `waving` | NJFL — upgrades Keen DLC reskins with real functionality. |
| `gitpush-mod/se-not-just-for-looks-additions` | `waving` | Extension pack for NJFL. |
| `gitpush-mod/se-not-just-for-looks-without-weapons` | `waving` | NJFL variant with weapon blocks removed. |
| `gitpush-mod/se-tiered-build-and-repair` | `waving` | Tiered Build-and-Repair mechanics. |
| `gitpush-mod/se-sg-core-mods` | `waving` | Bundle repo: 5 Sturmgrenadier Core mods. |
| `gitpush-mod/se-mod-adjuster-mods` | `waving` | Bundle repo: 10 balance adjustments for SG. |

### 🤖 MechWarrior 5 mods — `gitpush-mod` org

Palette: steel gray + combat orange/red (matches MechWarrior visual identity — heavy, industrial, warm accents).

| Repo | Capsule header | Notes |
|---|---|---|
| `gitpush-mod/mw5-zulibetterheroes-reforged` | `waving` | Reforged version of ZuluBetterHeroes. |
| `gitpush-mod/mw5-r13vergrrl` | `waving` | R13verGrrl — girlfriend addon mod. Scaffold only. |
| `gitpush-mod/mw5-knowledgebase` | `soft` | Reference/knowledge repo (not a mod itself). Softer palette to signal "docs, not gameplay". PRIVATE. |

### 🔧 SE tools + toolkits

Palette: same as SE mods (waving industrial).

| Repo | Capsule header | Notes |
|---|---|---|
| `Godimas101/universal-image-converter` | `waving` | Standalone SE texture/image conversion tool. |
| `Godimas101/universal-audio-converter` | `waving` | Standalone SE audio conversion tool. **Reference for Patreon Support section visual.** |
| `Godimas101/claude-engineers-maximum-immersion` | `waving` | Immersion / prompt utility for SE work. |
| `Godimas101/se-claude-skill` | `waving` | Space Engineers Claude skill / modding helper. |
| `Godimas101/space-engineers-modders-tool-kit` | `waving` | Toolkit and download hub. |

### 🚀 The Canadian Space — `The-Canadian-Space` org

| Repo | Capsule header | Notes |
|---|---|---|
| `The-Canadian-Space/tcs-tools` | `rect` | Public tools repo |
| `The-Canadian-Space/tcs-scripts` | `rect` | Public scripts / API helpers |
| `The-Canadian-Space/tcs-workflows` | `rect` | Private n8n workflow backups |
| `The-Canadian-Space/tcs-webpage` | `rect` | Private site codebase (planned) |
| `The-Canadian-Space/tcs-arcade` | `rect` | Private experiments (planned) |
| `The-Canadian-Space/tcs-docs` | `rect` | Internal wiki (Access-gated) |
| `The-Canadian-Space/tcs-public-wiki` | `rect` | Public marketing wiki |
| `The-Canadian-Space/tcs-archive` | `rect` | Historical dev artifacts (private) |
| `Godimas101/tcs-images` | `rect` | Article images (intentionally stays under Godimas101 — raw.githubusercontent.com URL stability) |

### 🛠️ Utility tools

| Repo | Capsule header | Notes |
|---|---|---|
| `Godimas101/claude-usage-monitor` | `slice` | Standalone desktop utility |
| `Godimas101/automatic-weight-recording` | `slice` | Standalone automation helper |

### 📚 Personal / Reference

| Repo | Capsule header | Notes |
|---|---|---|
| `Godimas101/personal-projects` | `venom` | Personal references, docs, and project index |
| `Godimas101/the-gold-mine` | `venom` | Curated external tools/docs inbox (private) |

### 👤 Org + user profile

| Repo | Capsule header | Notes |
|---|---|---|
| `Godimas101/Godimas101` | `blur` header + `soft` footer | Chris's personal profile README |
| `gitpush-mod/.github` | `blur` | Org profile for `gitpush-mod` — renders at github.com/gitpush-mod. Created 2026-07-14. Also hosts default community health files (bug_report, feature_request, config.yml, CONTRIBUTING.md, CODE_OF_CONDUCT.md) + org-wide workflows (auto-archive-mod-boards.yml, append-changelog.yml). |
| `The-Canadian-Space/.github` | `blur` | Org profile for TCS. Updated 2026-07-14 to style-guide compliance (was previously plain text). Palette: deep space → cyan → blue → purple. |
| `Godimas101/.github` | (special repo — no `profile/README.md`, personal profile lives at `Godimas101/Godimas101` instead) | Personal-account `.github` repo. Hosts shared workflows (`check-pat-expiration.yml`, `auto-archive-personal-projects.yml`), the PAT tracking manifest (`pats.json`), and default community health files (ISSUE_TEMPLATE, CONTRIBUTING, CODE_OF_CONDUCT) that all `Godimas101/*` repos inherit. Created 2026-07-14. |
| `voidput/.github` | (external to Chris's control) | SC-ORG-BOT lives here; not Chris's to style |

---

## Maintenance Notes

When adding a repo in future:

1. Decide which family it belongs to.
2. Add it to this file immediately (same PR as the new repo's README).
3. Use the assigned capsule type in its `README.md`.
4. If a new family is needed, define it in the Family Summary table first.

If there is ever a conflict between memory, habit, or an older README, **this file wins**.
