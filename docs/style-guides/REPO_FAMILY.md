# Repo Family Reference

This file is the **source of truth** for which `capsule-render` header family belongs to each repo.

When a new repo is created, renamed, split out, or rebranded, **update this file at the same time** as its `README.md`.

---

## Core Rule

- Every public repo should belong to a defined README family.
- The family determines the default `capsule-render` header style for that repo’s main `README.md`.
- If a repo needs an exception, document it here so future updates stay consistent.

---

## Family Summary

| Family | Default capsule type | Notes |
|---|---|---|
| Space Engineers | `waving` | Industrial / spacey palettes for mods, converters, toolkits, and modding-adjacent repos |
| The Canadian Space | `rect` | Dark-space base, per-repo accent colors, and `textBg=true` title highlighting |
| Tools | `slice` | Shared style for standalone utilities and small desktop/helper apps |
| Personal / reference | `venom` | Used for personal index/docs repos and reference-heavy collections |
| GitHub profile | `blur` | Profile header only; profile footer intentionally uses `soft` |

---

## Current Repo Assignments

### 🔧 Space Engineers

| Repo | Capsule header | Notes |
|---|---|---|
| `se-mods` | `waving` | Main Space Engineers mod collection |
| `se-claude-skill` | `waving` | Space Engineers Claude skill / modding helper |
| `space-engineers-modders-tool-kit` | `waving` | Toolkit and download hub |
| `universal-image-converter` | `waving` | Space Engineers texture/image conversion tool |
| `universal-audio-converter` | `waving` | Space Engineers audio conversion tool |

### 🚀 The Canadian Space

| Repo | Capsule header | Notes |
|---|---|---|
| `tcs-tools` | `rect` | Public tools repo |
| `tcs-scripts` | `rect` | Public scripts / API helpers |
| `tcs-images` | `rect` | Public image asset repo |
| `tcs-workflows` | `rect` | Private workflow repo |
| `tcs-webpage` | `rect` | Private site codebase |
| `tcs-arcade` | `rect` | Private experiments / side projects |

### 🛠️ Tools

| Repo | Capsule header | Notes |
|---|---|---|
| `claude-usage-monitor` | `slice` | Standalone desktop utility |
| `automatic-weight-recording` | `slice` | Standalone automation helper |

### 📚 Personal / Reference

| Repo | Capsule header | Notes |
|---|---|---|
| `personal-projects` | `venom` | Personal references, docs, and project index |

### 👤 Profile

| Repo | Capsule header | Notes |
|---|---|---|
| `Godimas101` | `blur` | Profile README header; keep the footer as `soft` unless deliberately changed |

---

## Maintenance Notes

When adding a repo in future:

1. Decide which family it belongs to.
2. Add it to this file immediately.
3. Use the assigned capsule type in its `README.md`.
4. If a new family is needed, define it here first.

If there is ever a conflict between memory, habit, or an older README, **this file wins**.
