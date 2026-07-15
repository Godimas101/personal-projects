# AGENTS.md — personal-projects

Chris's personal meta-repo. Holds docs, style guides, resumes, patreon assets, kitchen inventory, health tracking, and other 'my brain, but version controlled' content. Public but written for personal reference more than external audience.

## What this is

Chris's personal meta-repo. Holds docs, style guides, resumes, patreon assets, kitchen inventory, health tracking, and other 'my brain, but version controlled' content. Public but written for personal reference more than external audience.

## Where work lives (RULE — non-negotiable)

**Every task on this repo is a ticket on the [Personal Projects board](https://github.com/users/Godimas101/projects/2).** YOU (the agent) create the ticket BEFORE touching anything. No exceptions for "small" work.

Concrete rules — same as everywhere:

- **Starting work?** Open a ticket, add to the board, set Status = **In Progress**, then start.
- **Have an idea for later?** Ticket in **Backlog**. Not in memory, not in a README, not in NOTES.md.
- **Need Chris to check something before closing?** Move to **In QA** and comment what he needs to look at. Do NOT set to Done — that's Chris's call after review.
- **Finished + verified yourself?** Close the ticket with a closing summary (what you did / problems + solutions / anything NOT done).
- **Same-session micro-work?** Open + close in the same session — but the ticket exists.
- **Older than 30 days in Done?** The weekly cron moves it to Archived. The closed ticket persists.

Ticket body shape: see memory `[[feedback-ticket-body-shape]]` — What/Why → Acceptance → Related → Notes. Priority defaults to P2, Kind defaults to Feature.

## How to verify (before flagging In QA or closing)

- If touching docs: `mkdocs`-style style guides → build locally + eyeball. Style guides → cross-check that any example matches actual repo state.
- If touching health-tracking or patreon data: those get auto-committed by n8n workflows. Manual edits should be minimal + explained.
- If touching `docs/resumes/`: these are Chris's real job applications — extra care, don't invent job history.

## MUST NOT

- Touch `docs/resumes/CLAUDE.md` — it's gitignored personal content (per memory `[[reference-agents-md-hierarchy]]`, don't touch).
- Auto-commit to health-tracking or patreon folders — those have workflows that own the files.
- Rewrite Chris's WIP `README_STYLE_GUIDE.md` — he has uncommitted local changes there. Add to it, don't restructure it.

## Related

- Style guides: [`docs/style-guides/`](docs/style-guides/) — canonical for all repo READMEs
- Git infrastructure field guide: [`docs/git-infrastructure.md`](docs/git-infrastructure.md)
- Patreon supporters data: auto-populated by n8n daily
- Health tracking: auto-populated by [`automatic-weight-recording`](https://github.com/Godimas101/automatic-weight-recording)

---

*Part of Chris's `Godimas101` personal repos. Companion guide: [`personal-projects/docs/git-infrastructure.md`](https://github.com/Godimas101/personal-projects/blob/main/docs/git-infrastructure.md) covers the full infrastructure.*