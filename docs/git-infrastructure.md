# Git infrastructure — a field guide

Everything Chris + Claude have wired up for git, GitHub, boards, tokens, and automation across the mods + The Canadian Space + personal projects. **Read this before adding a new repo, rotating a PAT, wondering why an issue got filed automatically, or trying to add a new workflow that touches Chris's boards.**

Last updated: 2026-07-15.

---

## Table of contents

1. [The three GitHub owners](#the-three-github-owners)
2. [The `.github` special-repo convention](#the-github-special-repo-convention)
3. [Local folder layout](#local-folder-layout)
4. [Auto-workflows deployed](#auto-workflows-deployed)
5. [Project boards](#project-boards)
6. [Ticket-first workflow](#ticket-first-workflow)
7. [Personal Access Tokens (PATs)](#personal-access-tokens-pats)
8. [Memory system](#memory-system)
9. [The `/status` skill](#the-status-skill)
10. [Style guide + capsule-render](#style-guide--capsule-render)
11. [Hard-won incidents](#hard-won-incidents)
12. [Emergency recipes](#emergency-recipes)

---

## The three GitHub owners

Chris's work lives across three GitHub "owners" (accounts / orgs):

| Owner | Type | What lives there |
|---|---|---|
| [`Godimas101`](https://github.com/Godimas101) | User account | Chris's personal stuff — standalone tools, personal-projects meta-repo, the profile page, historical/one-off things |
| [`gitpush-mod`](https://github.com/gitpush-mod) | Organization | All published game mods (Space Engineers + MechWarrior 5) — separated from personal so mod contributors have a clean surface |
| [`The-Canadian-Space`](https://github.com/The-Canadian-Space) | Organization | The Canadian Space — automated aerospace news project. Docs, tools, workflows, arcade games. |

**Why the split?** Personal ≠ mod ≠ TCS. Each has a distinct audience, licensing footprint, and set of contributors. Also, `gitpush-mod` gives the mods a home that survives even if Chris someday rebrands or hands them off; TCS's org keeps the newsroom project professionally packaged.

**One exception:** [`Godimas101/tcs-images`](https://github.com/Godimas101/tcs-images) is intentionally NOT under the TCS org. Hundreds of live WordPress articles link to `raw.githubusercontent.com/Godimas101/tcs-images/…` paths. Moving the repo would 404 every published image. Leave it alone.

---

## The `.github` special-repo convention

GitHub has a magic convention: a repo named `.github` (literally starts with a dot) at the account/org level acts as a **defaults source** for everything else that account owns.

Chris has three of them:

- **[`Godimas101/.github`](https://github.com/Godimas101/.github)** — for personal repos
- **[`gitpush-mod/.github`](https://github.com/gitpush-mod/.github)** — for the gitpush-mod org
- **[`The-Canadian-Space/.github`](https://github.com/The-Canadian-Space/.github)** — for the TCS org

### What lives inside each

Two folders + optional top-level workflows:

```
<owner>/.github/
├── profile/
│   └── README.md       ← renders as the org landing page at github.com/<owner>
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md      ← inherited by every repo without its own
│   │   ├── feature_request.md
│   │   └── config.yml         ← disables blank issues, adds contact links
│   ├── workflows/             ← workflows that ONLY run in THIS special repo
│   │   └── whatever.yml
│   ├── CONTRIBUTING.md        ← inherited default
│   └── CODE_OF_CONDUCT.md     ← inherited default
├── LICENSE
├── README.md              ← for humans opening the .github repo itself
└── AGENTS.md              ← for agents editing this repo
```

**Special case:** `Godimas101/.github` has NO `profile/README.md`. Chris's personal profile lives at `Godimas101/Godimas101` (a user's profile repo has the same name as the user — separate GitHub convention). The `.github` version just holds defaults.

### How the inheritance works

Any repo under `<owner>/*` that doesn't have its own `.github/ISSUE_TEMPLATE/bug_report.md` uses the one from `<owner>/.github/.github/ISSUE_TEMPLATE/bug_report.md`. Same for `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, etc. Only overridden per-repo if you drop a same-named file in that repo's own `.github/` folder.

---

## Local folder layout

On Chris's machine, all his working repos live under `C:\Users\Chris Carpenter\VS Code Projects\`. The structure (as of 2026-07-15):

```
VS Code Projects/
├── AGENTS.md                   ← top-level Golden Rules for all agents
├── mods/                       ← game mods (SE + MW5)
│   ├── AGENTS.md                    (nav aid — points to per-mod AGENTS.md)
│   ├── se-infolcd-apex-update/      → gitpush-mod/se-infolcd-apex-update
│   ├── se-infolcd-apex-advanced/    → gitpush-mod/se-infolcd-apex-advanced
│   ├── se-not-just-for-looks/       → gitpush-mod/se-not-just-for-looks
│   ├── se-not-just-for-looks-additions/
│   ├── se-not-just-for-looks-without-weapons/
│   ├── se-tiered-build-and-repair/
│   ├── se-sg-core-mods/             (bundle of 5 mods in subfolders)
│   ├── se-mod-adjuster-mods/        (bundle of 10 mods in subfolders)
│   ├── mw5-zulibetterheroes-reforged/
│   ├── mw5-r13vergrrl/              (scaffold — R13verGrrl pilot mod)
│   ├── mw5-knowledgebase/           (READ FIRST for MW5 work — private)
│   ├── mw5-tools/
│   └── space-engineers-tools/       (standalone SE tools, various remotes)
│
├── github-settings/            ← all the .github + profile repos (2026-07-15+)
│   ├── gitpush-mod/                 → gitpush-mod/.github
│   ├── godimas-defaults/            → Godimas101/.github (auto-workflows + defaults)
│   ├── godimas-profile/             → Godimas101/Godimas101 (profile page)
│   └── the-canadian-space/          → The-Canadian-Space/.github
│
├── tcs-arcade/                 ← TCS games (2026-07-15+)
│   ├── idle-launch/                 → The-Canadian-Space/idle-launch (private)
│   └── autodoom/                    → The-Canadian-Space/autodoom (private)
│
├── n8n-projects/
│   └── the-canadian-space/     ← TCS working directory
│       ├── AGENTS.md                (top-level TCS rules — untracked local file)
│       ├── tcs-tools/               → The-Canadian-Space/tcs-tools
│       ├── tcs-scripts/             → The-Canadian-Space/tcs-scripts
│       ├── tcs-public-wiki/         → The-Canadian-Space/tcs-public-wiki
│       ├── tcs-docs/                → The-Canadian-Space/tcs-docs (private)
│       ├── tcs-workflows/           → The-Canadian-Space/tcs-workflows (private)
│       ├── tcs-archive/             → The-Canadian-Space/tcs-archive (private)
│       ├── tcs-webpage/             → The-Canadian-Space/tcs-webpage (private)
│       └── tcs-images/              → Godimas101/tcs-images (intentional)
│
├── personal-projects/          → Godimas101/personal-projects
│   ├── docs/
│   │   ├── style-guides/            ← README + REPO_FAMILY reference
│   │   └── git-infrastructure.md    ← THIS FILE
│   └── patreon/                     ← supporter data + button images
│
└── discord-bots/               ← various Discord bot projects (own remotes)
```

**Why `github-settings/` as a top-level sibling?** So all the "GitHub settings"-flavored repos are in one visually distinct folder, not scattered inside `mods/`. Makes it obvious what they are.

---

## Auto-workflows deployed

There are five categories of automation running across Chris's repos. All the ORG-wide + USER-wide workflows live in the corresponding `.github` repos.

### 1. Auto-archive old Done items on boards

Moves items sitting in `Done` for > 30 days to `Archived`. Keeps boards clean; the tickets + their CHANGELOG entries persist forever.

| Workflow | Repo | Scope | Schedule |
|---|---|---|---|
| `auto-archive-mod-boards.yml` | [`gitpush-mod/.github`](https://github.com/gitpush-mod/.github) | All 10 mod boards (projects/3-12) | Sun 05:00 UTC |
| `auto-archive-personal-projects.yml` | [`Godimas101/.github`](https://github.com/Godimas101/.github) | Personal Projects (users/Godimas101/projects/2) | Sun 05:00 UTC |

Both dispatch-able manually with `dry_run=true` + `days_old=<N>` inputs for testing.

### 2. Auto-CHANGELOG on issue close

When an issue is closed as "completed" on a mod repo, an entry gets appended to that repo's `CHANGELOG.md` in Keep-a-Changelog format under `## [Unreleased]`.

**Wiring:**
- **Reusable workflow:** [`gitpush-mod/.github/.github/workflows/append-changelog.yml`](https://github.com/gitpush-mod/.github/blob/main/.github/workflows/append-changelog.yml) — the actual logic
- **Caller stub:** each mod repo has `.github/workflows/on-issue-close.yml` (~15 lines) that invokes the reusable workflow with `secrets: inherit`

**Deployed to (as of 2026-07-15):** all 10 mod repos under gitpush-mod. NOT deployed to games, TCS, or Godimas101 tools by default.

**Security note:** issue title is user-controlled on public repos → passed to Python via env var, never interpolated into a script body. Only fires on `state_reason=completed` (skips "not planned" closures).

### 3. Weekly status digest

Every Monday 06:00 UTC, aggregates state from all 14 boards into ONE issue on [`Godimas101/.github`](https://github.com/Godimas101/.github/issues?q=is:issue+label:weekly-digest). Shows:
- **In Progress** across all boards
- **In QA** across all boards (⚠️ marker if any have sat > 3 days)
- **Recently Done** (last 7 days)

Closes the previous week's digest automatically so only the current week's is open. Manual re-run: **Actions → Weekly status digest → Run workflow**.

Workflow: [`Godimas101/.github/.github/workflows/weekly-digest.yml`](https://github.com/Godimas101/.github/blob/main/.github/workflows/weekly-digest.yml).

### 4. PAT expiration reminder

Weekly Mondays 05:00 UTC. Reads [`Godimas101/.github/pats.json`](https://github.com/Godimas101/.github/blob/main/pats.json), computes days-to-expiry for each PAT, files an issue if any is:
- Within 60 days of expiry, OR
- Has `expires: UNKNOWN`

Workflow: `check-pat-expiration.yml`. Uses default `GITHUB_TOKEN` for filing issues (no PAT dependency — avoids the recursion of "PAT to warn about PATs").

### 5. Quarterly AGENTS.md link check

1st of Jan/Apr/Jul/Oct at 05:00 UTC. Discovers all repos across the 3 owners, fetches each `AGENTS.md`, extracts URLs, tests them in parallel (10s timeout each). Files an issue on `Godimas101/.github` if any dead links. Catches drift when a repo moves, a board number changes, or a memory file gets renamed.

Workflow: `agents-linkcheck.yml`. Manual dry-run available via workflow_dispatch.

---

## Project boards

Chris uses GitHub Projects V2 boards for everything. Structure (as of 2026-07-15):

### Boards catalog

| # | Owner | Board | Purpose |
|---|---|---|---|
| 1 | user Godimas101 | (n/a) | *reserved* |
| **2** | user Godimas101 | [Personal Projects](https://github.com/users/Godimas101/projects/2) | Everything Godimas101 + cross-cutting personal work |
| 1 | org The-Canadian-Space | [TCS Timeline](https://github.com/orgs/The-Canadian-Space/projects/1) | All TCS work — shared across every TCS repo |
| 2 | org The-Canadian-Space | [Idle Launch](https://github.com/orgs/The-Canadian-Space/projects/2) | The first TCS arcade game |
| 3 | org The-Canadian-Space | [AutoDoom](https://github.com/orgs/The-Canadian-Space/projects/3) | The second TCS arcade game |
| 3 | org gitpush-mod | [InfoLCD Apex Update](https://github.com/orgs/gitpush-mod/projects/3) | Flagship SE mod |
| 4 | org gitpush-mod | [InfoLCD Apex Advanced](https://github.com/orgs/gitpush-mod/projects/4) | Sibling SE mod |
| 5 | org gitpush-mod | [Not Just For Looks](https://github.com/orgs/gitpush-mod/projects/5) | SE mod |
| 6 | org gitpush-mod | [NJFL — Additions](https://github.com/orgs/gitpush-mod/projects/6) | SE mod |
| 7 | org gitpush-mod | [NJFL — Without Weapons](https://github.com/orgs/gitpush-mod/projects/7) | SE mod |
| 8 | org gitpush-mod | [Tiered Build and Repair](https://github.com/orgs/gitpush-mod/projects/8) | SE mod |
| 9 | org gitpush-mod | [SG Core Mods](https://github.com/orgs/gitpush-mod/projects/9) | SE bundle repo |
| 10 | org gitpush-mod | [Mod Adjuster Mods](https://github.com/orgs/gitpush-mod/projects/10) | SE bundle repo |
| 11 | org gitpush-mod | [ZuluBetterHeroes Reforged](https://github.com/orgs/gitpush-mod/projects/11) | MW5 mod |
| 12 | org gitpush-mod | [R13verGrrl](https://github.com/orgs/gitpush-mod/projects/12) | MW5 mod (scaffold) |

**Total: 14 boards.** All queried by the weekly digest workflow.

### Standard Status field (7 states)

Every board uses the same Status column values:

| Status | Color | When |
|---|---|---|
| **Backlog** | gray | Idea captured, not prioritised |
| **Todo** | blue | Prioritised, ready to pick up |
| **In Progress** | yellow | Actively being worked on |
| **In QA** | purple | Coded, awaiting Chris's review (never set by Done-yourself agents — this means "your turn") |
| **Blocked** | red | Waiting on something external |
| **Done** | green | Complete — auto-CHANGELOG triggers |
| **Archived** | gray | Auto-archived after 30 days in Done |

### Standard custom fields

- **Priority** — P0 (critical) / P1 (high) / P2 (normal, default) / P3 (someday)
- **Kind** — Feature (default) / Bug / Chore / Design / Investigation / Milestone

Both are optional but filled in by default when agents use the ticket body shape (see below).

---

## Ticket-first workflow

**Every task on any of Chris's boards starts with a ticket.** The agent creates the ticket BEFORE touching anything. No exceptions for "small" work.

### The six cases (established across all boards)

1. **Starting work?** Create the ticket, set Status = **In Progress**, then start.
2. **Idea for later?** Ticket in **Backlog**. Not in memory, not in a README, not in NOTES.md.
3. **Need Chris to check something?** Move to **In QA** and comment what he needs to look at. Do NOT set to Done.
4. **Finished + verified yourself?** Close the ticket with a structured closing summary.
5. **Worth announcing publicly?** After the ticket is closed, add a hand-authored post to the public wiki's big-moments blog (TCS only).
6. **Older than 30 days in Done?** Weekly cron moves it to Archived. Ticket + CHANGELOG entry persist.

### Ticket body shape (agents follow this)

```markdown
## What / Why
<1-3 sentences on what needs to happen and the reason>

## Acceptance criteria
- [ ] <specific, checkable outcome>
- [ ] ...

## Related
- Related tickets, memory entries, repos, paths

## Notes
<optional context>
```

Priority defaults to **P2**, Kind defaults to **Feature**. Full spec in memory `[[feedback-ticket-body-shape]]`.

### Closing summary shape

Every close, on every board, includes:

- **What we did** (bulleted)
- **Problems + solutions** (if any)
- **Anything NOT done** (be honest — future-you will want to know)

Full spec in memory `[[reference-ticket-close-comments]]`.

---

## Personal Access Tokens (PATs)

Chris uses three PATs, all documented in [`Godimas101/.github/pats.json`](https://github.com/Godimas101/.github/blob/main/pats.json). The weekly workflow reads this file and warns if any are close to expiry.

### The three PATs

| Name | Type | Scope | Where installed | Renew URL |
|---|---|---|---|---|
| **MOD_PROJECT_TOKEN** | Fine-grained | Organization → Projects (Read+Write) on gitpush-mod | Org secret on `gitpush-mod` (visibility=all) | [Fine-grained PATs](https://github.com/settings/tokens?type=beta) |
| **PERSONAL_PROJECT_TOKEN** | Classic (`project` + `repo`) | User account + org projects Chris can see | Repo secret on `Godimas101/.github` | [Classic PATs](https://github.com/settings/tokens) |
| **TCS_PROJECT_TOKEN** | Fine-grained (assumed) | Organization → Projects on The-Canadian-Space + repo Contents/Issues | Org secret on `The-Canadian-Space` OR repo secret on `tcs-docs` | [Fine-grained PATs](https://github.com/settings/tokens?type=beta) |

### Why a classic PAT for the personal one?

Fine-grained PATs currently DON'T expose user-level Projects V2 access in the account permissions dropdown (for Chris's account, as of 2026-07). Classic PATs support user Projects V2 via the `project` scope — so `PERSONAL_PROJECT_TOKEN` is a classic PAT with `project + repo`.

### Installing a PAT the safe way

**Windows-specific trick — see memory `[[reference-gh-secret-from-clipboard]]`.** The one-liner that works from Git Bash:

```bash
powershell.exe -NoProfile -Command "Get-Clipboard" | tr -d '\r\n' | gh secret set <NAME> --org <ORG> --visibility all
# or for repo-scoped:
powershell.exe -NoProfile -Command "Get-Clipboard" | tr -d '\r\n' | gh secret set <NAME> -R <owner>/<repo>
```

**Critical:** the `tr -d '\r\n'` is not optional. Windows clipboard content ships with `\r\n` line endings; without stripping them, they land IN the secret value and every future auth attempt returns HTTP 401 Bad credentials.

**NEVER use bash `$(...)` command substitution to grab the clipboard from Git Bash** — the substitution silently fails on Windows and stores the literal string `"Get-Clipboard..."` as the secret value. Been there, spent an hour debugging.

### Rotating a PAT

1. Generate new token at the relevant GitHub URL (fine-grained or classic)
2. Copy to clipboard
3. Run the safe-install one-liner above with the same secret name
4. Update the `created` + `expires` dates in `Godimas101/.github/pats.json` and commit
5. Verify by triggering a workflow that uses that secret (e.g. weekly digest for `PERSONAL_PROJECT_TOKEN`)

### Verifying a PAT works

There's no manual "test my PAT" step — the auto-workflows will catch a broken token on their next scheduled run and file an issue. For an on-demand check, trigger the diagnostic workflow that was written during the 2026-07-14 setup (see git history on `.github` repos for the pattern).

---

## Memory system

Chris uses Claude Code's file-based memory system. Files live at `C:\Users\Chris Carpenter\.claude\projects\d--claude-mem\memory\`.

**Note the home:** `d--claude-mem`, not any game slug. If a session's memory directory looks empty, Chris is running Claude Code from a different working directory than `D:\claude-mem` — see `[[reference-claude-mem-home-base]]`.

### Memory types

- **user** — Chris's role, goals, knowledge (auto-consulted when framing responses)
- **project** — active initiatives, in-flight decisions, historical context
- **reference** — durable pointers (paths, tools, patterns) that don't change often
- **feedback** — validated preferences and rules of engagement Chris has stated

### Key reference memories to know about

- `[[reference-agents-md-hierarchy]]` — where every AGENTS.md file lives + the board→repo mapping
- `[[reference-agents-md-building-rules]]` — rules for constructing new AGENTS.md files
- `[[reference-readme-style-guide]]` — pointer to the canonical style guide
- `[[reference-playwright-visual-verification]]` — Playwright pattern for screenshotting visual work
- `[[reference-gh-secret-from-clipboard]]` — PAT install pattern (see above)
- `[[reference-ticket-close-comments]]` — closing-summary structure
- `[[feedback-ticket-body-shape]]` — ticket-filing structure
- `[[feedback-tcs-ticket-first]]` — ticket-first rule for TCS
- `[[feedback-token-spend-during-dev]]` + `[[feedback-workflow-efficiency]]` — how much token spend to lean into per task
- `[[feedback-git-author-email]]` — git commits use `rustygear@hotmail.com`, NEVER `chris.carpenter@prodigygame.com`

Full index at `~/.claude/projects/d--claude-mem/memory/MEMORY.md`.

---

## The `/status` skill

At `~/.claude/skills/status/SKILL.md`. When Chris types `/status`, Claude:

1. Runs `pwd + git status + git log --oneline -5` to see local state
2. Looks up the associated project board via the repo→board mapping (in the skill file)
3. Queries **In Progress + In QA + Backlog top-5** for THAT board
4. Reads the latest weekly digest issue on `Godimas101/.github` for the global In QA list
5. Checks open **PAT reminder** + **linkcheck** issues on `Godimas101/.github`
6. Presents a scannable "here's where you were" summary + a suggested-next-move one-liner

Runs at session start (or when Chris says "where were we"). The skill file has explicit anti-patterns ("don't list all closed tickets", "don't ask Chris what he wants — infer + suggest").

---

## Style guide + capsule-render

Canonical style at [`personal-projects/docs/style-guides/README_STYLE_GUIDE.md`](style-guides/README_STYLE_GUIDE.md). Family map at [`REPO_FAMILY.md`](style-guides/REPO_FAMILY.md).

### Current capsule alignment (2026-07-15+)

Every capsule-render header uses these values for a properly-centered title with description just below the black `textBg` pill:

- `height=200`
- `fontAlignY=42` (title vertically centered)
- `descAlignY=68` (description just below the pill)
- `fontSize=30`
- `descSize=17` (or 15 for longer descriptions)

If you see `fontAlignY=35, descAlignY=57` on an older README, that's the pre-fix alignment — description overlapped the pill. Update.

### Family → capsule type

- **Space Engineers mods** → `waving`, deep blue palette (`0:0B1021,45:2563EB,100:7C3AED`)
- **MechWarrior 5 mods** → `waving`, steel-gray + combat-orange palette (`0:1F2937,45:78716C,100:F97316`)
- **SE + MW5 games / arcade** → `rect` with `textBg=true`, TCS-adjacent palettes per game
- **TCS repos** → `rect` with `textBg=true`, deep space + per-repo accent
- **Utility tools** → `slice`, warm/amber palettes
- **Personal + reference** → `venom`, cool + moody
- **Org profile pages** → `blur`, family-appropriate palette
- **Chris's personal profile** (`Godimas101/Godimas101`) → `blur` header + `soft` footer

---

## Hard-won incidents

Things that broke and cost time. Documented so future-us doesn't repeat them.

### The `Get-Clipboard` PAT install trap (2026-07-14)

**Symptom:** Every workflow using `MOD_PROJECT_TOKEN` returned HTTP 401 Bad credentials. Local `gh` calls worked fine (different token).

**Root cause:** the initial install command ran via `$(powershell -Command Get-Clipboard)` from Git Bash. Bash's command substitution silently failed to execute PowerShell on Windows and stored the LITERAL STRING `"Get-Clipboard..."` (82 chars) as the secret value.

**Fix:** use the pipe pattern documented above in [PATs](#personal-access-tokens-pats).

### Fine-grained PAT missing user Projects (2026-07-14)

**Symptom:** `PERSONAL_PROJECT_TOKEN` returned HTTP 200 for `/user` but `{"data":{"user":{"projectV2":null}}}` for user projects.

**Root cause:** fine-grained PATs don't expose "Projects" in the account permissions dropdown for Chris's account setup.

**Fix:** use a **classic PAT** with `project + repo` scopes for user projects. Fine-grained PATs still fine for org projects (like `MOD_PROJECT_TOKEN`).

### 12-char PAT prefix leak in diagnostic logs (2026-07-14)

**Symptom:** during troubleshooting, a diagnostic workflow printed the first 12 chars of each PAT to public run logs.

**Assessment:** GitHub secret-scanning masks the FULL secret value only, not substrings. 12 of 40 chars = 28 chars of remaining entropy ≈ still uncrackable — but bad hygiene.

**Fix:** rotated both tokens 2026-07-15. Any future diagnostic that touches a secret value should redact prefixes too.

### VS Code file locks during folder rename (2026-07-14, 2026-07-15)

**Symptom:** `mv` failed with "Permission denied" when moving folders under `mods/` or `Godimas101/` (bash), or "You do not have sufficient access rights" (PowerShell Move-Item).

**Root cause:** VS Code holds file handles on open workspaces. Some Move-Item operations partial-succeed (metadata moves, working files don't).

**Fix:** use `robocopy /MOVE` for stubborn cases — it handles locked files better than mv/Move-Item. Recovery from a partial move: destination `.git` is intact, so `git restore .` in the destination brings tracked files back from HEAD, then remove any remaining source files.

### DraftIssue has no `url` field (2026-07-15)

**Symptom:** weekly digest workflow's GraphQL query failed with `"Field 'url' doesn't exist on type 'DraftIssue'"` on every board.

**Root cause:** GitHub Projects V2 draft issues are internal to the board and don't have public URLs. Regular Issues have `url`, DraftIssues don't.

**Fix:** in the query, only ask for `url` on Issue + PullRequest types. Fall back to the board's own URL when linking a draft issue.

### Recreating `Status` field options orphans existing items (2026-07-14)

**Symptom:** items previously set to "Done" showed as "(no status)" after adding a new option like "Archived".

**Root cause:** `updateProjectV2Field` with a new `singleSelectOptions` list REPLACES the entire options list. Without passing existing IDs, GraphQL generates new option IDs, which don't match items' old assignments.

**Fix:** always pass existing option IDs when updating a `singleSelectOptions` list. New options can be added alongside without breaking assignments.

---

## Emergency recipes

Quick copy-paste recipes for common ops.

### "I need to know what state my boards are in RIGHT NOW"

Manual-trigger the weekly digest:

```bash
gh workflow run weekly-digest.yml -R Godimas101/.github
# Then wait ~30s and open:
# https://github.com/Godimas101/.github/issues?q=is:issue+label:weekly-digest
```

### "A PAT is not working — is it corrupted?"

Trigger the diagnostic workflow if it still exists in git history on `gitpush-mod/.github`. Or run this locally:

```bash
# Substitute your token
export TEST_TOKEN='<the token to test>'
curl -sS -w "HTTP %{http_code}\n" \
  -H "Authorization: Bearer $TEST_TOKEN" \
  https://api.github.com/user | head -20
```

Expect HTTP 200 with your login info. HTTP 401 = bad token.

### "I want to add a new mod repo to gitpush-mod"

1. Create the repo on GitHub (via `gh repo create gitpush-mod/<name> --public`)
2. Add to REPO_FAMILY.md
3. Create a project board (script pattern at `scratchpad/mod-batch/create_boards.py` — adapt)
4. Add `AGENTS.md + CLAUDE.md + LICENSE + .gitignore + README` following the templates
5. Add `.github/workflows/on-issue-close.yml` (caller stub) for auto-CHANGELOG
6. Update `Godimas101/.github/.github/workflows/weekly-digest.yml` BOARDS array + `mods/AGENTS.md` nav table

### "I want to add a new agent-checked repo somewhere else"

Same as above but skip the on-issue-close if not appropriate. Add the repo to the `OWNERS` list in `agents-linkcheck.yml` if the repo is under an owner not already covered.

### "A memory file got renamed / moved and now `[[link]]` references are stale"

The quarterly link-check workflow catches HTTP-URL drift. For `[[memory-name]]`-style links (which aren't URLs), grep for the old name across all memory files + AGENTS.md files:

```bash
grep -rn "old-memory-name" ~/.claude/projects/d--claude-mem/memory/
grep -rn "old-memory-name" "C:/Users/Chris Carpenter/VS Code Projects/" --include=AGENTS.md
```

### "I need to close a bunch of tickets in bulk"

Use the pattern in `scratchpad/mod-batch/audit_close.py` — reads a list of `(item_id, note)` tuples, appends closing note to each ticket's body, sets Status = Done.

---

## Related docs

- [Style guide](style-guides/README_STYLE_GUIDE.md) — README conventions
- [REPO_FAMILY](style-guides/REPO_FAMILY.md) — capsule family per repo
- Memory: `~/.claude/projects/d--claude-mem/memory/MEMORY.md`
- Skills: `~/.claude/skills/status/SKILL.md`

---

*Written 2026-07-15 as part of the "Godimas101 sweep + git-infrastructure doc" batch. Update this file when the setup changes — don't let the reality drift away from the map.*
