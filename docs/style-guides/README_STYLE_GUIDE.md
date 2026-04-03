# README Style Guide

Use this guide for any **public-facing `README.md`** in this workspace — especially anything that may end up on GitHub.

> **Goal:** keep the docs technically solid, visually polished, and recognizably human.

This file is the source of truth for public README tone, structure, layout, and visual enhancement choices.

---

## Core Principle

**Accuracy first, personality second, polish third.**

The fun layer is welcome, but it should never hide or weaken the real technical content. Setup steps, requirements, warnings, commands, compatibility notes, and limitations should stay clear and exact.

A beautiful README that is confusing is still a bad README.

---

## Locked-In House Style

These are the default standards we want to follow across public docs.

### Always do this
- use a clear, polished **title line** — for public repo pages in this workspace, default to a **capsule-render header**
- keep an identifiable **emoji + project name** in the visible title treatment or directly below it if needed
- add a short, human-sounding tagline blockquote under the title line
- keep section headers scannable and emoji-led where appropriate
- explain the project quickly before getting clever
- preserve real technical detail even when the prose is playful

### Allowed level-ups
- themed icons
- tasteful badges
- screenshots or GIFs when they clarify something
- tables for dense information
- banner/header art for flagship pages
- dynamic cards/widgets when they add real signal

### Use with restraint
- animations
- large badge walls
- novelty widgets
- centered layouts for long text
- decorative art that does not help comprehension

---

## Visual Design Philosophy

### 1. Signal over clutter
Every visual element should either:
- improve scanning
- reinforce the theme
- showcase useful information
- add a bit of charm without getting in the way

If it does none of those things, cut it.

### 2. One visual system per README
If we use icons, headers, and badges, they should look like they belong together.

Do **not** mix:
- flat line icons with glossy 3D icons
- monochrome icons with neon sticker art
- five different badge styles in the same header
- multiple conflicting capsule-render styles in the same README

#### README family rule
Different **families of READMEs** should use different overall capsule-render patterns so the projects feel related-but-distinct.

Examples of families:
- **tool repos**
- **mod collections**
- **automation/workflow repos**
- **toolkits / landing pages**
- **profile README**

Within one family, keep the capsule style consistent.
Across different families, vary the overall pattern — for example by changing `type=` (`waving`, `rounded`, `rect`, `soft`), composition style, and color mood.

**Goal:** recognizable visual identity without every repo header feeling copy-pasted.

**Current family direction in this workspace**
- **Space Engineers repos** — shared `waving` capsule headers with industrial / spacey accent palettes
- **The Canadian Space repos** — shared `rect` capsule headers with a dark-space base, per-repo accent colors, and `textBg=true` title highlighting
- **Toolkits / landing pages** — can be a bit bolder, but should still stay consistent within their own family

### 3. The top of the README does the heavy lifting
The first screenful should answer:
- what is this?
- why should I care?
- what kind of project is it?
- where do I go next?

### 4. Style should match project scale
- **Small utility repo** → simple title, tagline, concise sections
- **Flagship repo / toolkit** → more visual polish, maybe banner art
- **GitHub profile README** → most room for layout, cards, icon rows, and visual personality

---

## Required Style Elements

### 1. Title
- For **public repo READMEs in this workspace**, the title line should default to a **capsule-render header**
- The header should still clearly identify the project name, and may include an emoji, subtitle, or short descriptor
- A pun, joke, or playful name is encouraged when it fits
- Keep it readable; do not make the title treatment so goofy that the project becomes hard to identify

**Preferred pattern**
```md
<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&height=170&color=0:0B1021,45:2563EB,100:7C3AED&text=Project%20Name&fontColor=ffffff&fontAlignY=35&fontSize=32&desc=Short%20descriptor%20here&descAlignY=57&descSize=18" />
</p>
```

**Good examples**
- capsule header for `🚀 TCS Workflows`
- capsule header for `🛠️ Space Engineers Mods`
- capsule header for `🛰️ Orbit Ops Toolkit`

### 2. Tagline
Directly under the title, include a short blockquote in this pattern:

```md
> **"A witty, human-sounding one-liner that explains the project without sounding like a press release."**
```

Guidelines:
- 1 sentence
- playful, conversational, or self-aware
- still communicates what the project actually does

### 3. Section Headers
Use emojis on major section headers.

**Examples**
- `## ✨ Features`
- `## 🚀 Getting Started`
- `## 🔧 Installation`
- `## 📁 Project Structure`
- `## 🧪 Testing`
- `## 📝 Notes`

### 4. Tone
Public READMEs should feel:
- casual
- conversational
- lightly witty
- confident but not salesy
- written by a smart human, not a startup landing page generator

Avoid:
- corporate jargon
- hype language
- fake marketing voice
- forced jokes every paragraph

### 5. Quick Start
When a project can be downloaded, installed, launched, or tried quickly, include a `## 🚀 Quick Start` section near the top.

**Purpose:** help a visitor get from “what is this?” to “cool, I can use it” in a few seconds.

**Best format**
- short numbered list
- 2–5 steps max
- link directly to the most likely next action
- keep it practical and friction-free

**Good use cases**
- downloadable tools
- utilities with a simple install/run flow
- starter repos
- modding toolkits
- anything where the reader benefits from a fast on-ramp

### 6. Footer
If it fits, end with a short italicized closing line or pun.

**Example**
```md
*Thanks for stopping by — now go build something gloriously overengineered.*
```

This is optional, but encouraged for public repos.

### 7. Support section (when relevant)
If the project is free, community-supported, creator-funded, or tied to ongoing tools/mods/content, include a `## 🧡 Support` section near the bottom of the README.

**Best placement**
- after the main content
- before the final italic sign-off
- as the last real section on the page

Use it for:
- Patreon or Ko-fi links
- donation/support buttons
- gentle community support asks for free tools
- links that help fund continued updates

**Standard support button**
When a support section is included, it should use this Patreon button unless there is a project-specific reason not to:

```md
[![Support on Patreon](https://raw.githubusercontent.com/Godimas101/personal-projects/main/patreon/images/buttons/patreon-medium.png)](https://patreon.com/Godimas101)
```

Keep the surrounding copy brief, appreciative, and low-pressure.

---

## Recommended README Structure

Not every README needs every section, but this is the default pattern:

1. **Title**
2. **Tagline blockquote**
3. **Short overview / what this repo is**
4. **Quick Start** if the repo has a fast path to use
5. **Features / highlights**
6. **Setup / installation**
7. **Usage / workflow / examples**
8. **Project structure or contents**
9. **Notes, caveats, or current status**
10. **Support / sponsorship** if relevant
11. **Credits / links** if relevant
12. **Optional italicized footer**

---

## Visual Level-Ups for Public READMEs

### Banners and title lines
For public-facing repo pages in this workspace, a **`capsule-render` title line is now the default**.

This is especially important for **tool repos**, **toolkits**, **landing-page-style docs**, and anything meant to feel polished on GitHub. The `space-engineers-modders-tool-kit` README is the model to follow here.

**Rule of thumb:**
- use a capsule-render header for public project READMEs by default
- use stronger banner treatment for toolkits, flagship repos, and profile pages
- only fall back to a plain Markdown title when the page is intentionally minimal or purely internal

### Capsule-render guidance
Based on the `kyechan99/capsule-render` reference, we want to use it in a controlled, branded way.

**Preferred usage**
- choose one capsule family per README: `waving`, `soft`, `rounded`, or `rect`
- use moderate height (`120`–`180` for project pages, `160`–`220` for profile pages)
- use `theme=` or explicit brand colors for consistency
- use one header, optionally one footer
- keep a shared look **within** a README family, but use a **different capsule family** for different repo families

**Example family mapping**
- **tool repos** → `waving`
- **mod collections** → `rounded` or `soft`
- **automation/workflow repos** → `rect`
- **toolkits / landing pages** → `waving` or `rect` with more polish
- **profile README** → the most expressive treatment, but still coherent

**Avoid**
- stacking multiple competing capsule renders
- random colors on pages that need a fixed identity
- over-animated headers that distract from the content
- making every repo use the exact same capsule type and composition

**Starter snippet**
```md
<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&height=160&section=header&text=Project%20Name&fontAlignY=35&fontSize=42&theme=radical" />
</p>
```

**Important note**
The reference repo notes the service is **best-effort**. If we ever depend on it heavily for a high-traffic or long-lived page, self-hosting/forking is the safer option.

### Icons
Icons are good when they make a page easier to scan.

**Use icons for**
- contact links
- technology stacks
- feature categories
- platform/tool indicators

**Do not use icons for**
- every single bullet
- decoration with no meaning
- inconsistent visual noise

#### Themed icon rule
If we use icons, they should be from the **same visual family** or at least from compatible families.

Preferred sources for dev/tool icons:
- `simple-icons`
- `devicon`
- `shields.io` badges
- other clean SVG sets with consistent style

`Freepik` can be useful for more decorative iconography or illustrations, but:
- check the license/attribution requirements first
- prefer SVG or transparent PNG assets
- make sure the style matches the rest of the page
- test legibility in both dark and light GitHub themes

### Badges
Badges are useful in moderation.

**Good badge uses**
- version
- license
- build/test status
- platform support
- release channel

**Badge rule:** keep the header badge row tight. Usually **3–6 badges max** is enough.

### Screenshots and GIFs
Use screenshots/GIFs when they explain the product, UI, workflow, or vibe faster than text.

**Best practices**
- one strong screenshot beats five mediocre ones
- crop tightly
- keep backgrounds clean
- add short captions if needed
- use GIFs only when motion matters

---

## Dark/Light Theme Compatibility

If a README includes visual assets, it must look acceptable in both GitHub themes.

### Default rule
Prefer:
- transparent backgrounds
- SVG where possible
- icon sets that work on both dark and light backgrounds

### When theme-specific assets are needed
Use GitHub’s theme-aware image patterns.

**Option A: theme context tags**
```md
![Dark version](image-dark.svg#gh-dark-mode-only)
![Light version](image-light.svg#gh-light-mode-only)
```

**Option B: `<picture>` element**
```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./dark-card.svg">
  <source media="(prefers-color-scheme: light)" srcset="./light-card.svg">
  <img alt="Profile card" src="./light-card.svg">
</picture>
```

This is especially relevant for stat cards, banners, and any custom image assets.

---

## Dynamic Widgets and Embedded Cards

Dynamic components can make a README feel alive, but they should be treated as **enhancements**, not the backbone of the page.

### GitHub Readme Stats
From `anuraghazra/github-readme-stats`, the most useful components for us are:
- stats card
- top languages card
- pinned repo cards
- optional WakaTime card

**Recommended use**
- mostly for the future **profile README**
- possibly for a top-level personal landing repo
- not necessary for every project repo

**Preferred styling**
- `theme=transparent` when possible
- or pair dark/light variants using theme-aware image methods
- `show_icons=true` for better scanability
- compact layouts for language cards

**Useful note from the reference**
The public Vercel endpoint is **best-effort** and can hit rate limits. For more reliable use, the repo recommends **GitHub Actions** or **self-hosting**.

### Contribution art / `github_painter`
From `mattrltrent/github_painter`, contribution graph art is a fun optional flourish for a **profile README**, not a normal project README element.

**Use only if**
- it fits the personality of the profile
- we are okay with it being decorative/novelty-driven
- it does not make the profile feel gimmicky

**Cautions from the reference**
- better to use a new empty private repo while testing
- check the generated script before running it
- it is explicitly a use-at-your-own-risk kind of tool

**House recommendation:** optional for profile, never required.

---

## GitHub Profile README Section

This section is specifically for the upcoming profile README.

### What a profile README should be
A profile README is not just a bio dump. It is a **personal landing page**:
- part intro
- part portfolio
- part status board
- part vibe check

### Setup reminder
To create a GitHub profile README, the repo must be:
- **public**
- named exactly the same as the GitHub username
- contain a `README.md`

### Recommended profile layout
This is the default structure we should aim for:

1. **Hero banner**
   - capsule-render title line
   - short intro or signature phrase

2. **Quick identity section**
   - who you are
   - what you build
   - what themes/projects you care about

3. **Link/icon row**
   - GitHub
   - Patreon / site / relevant socials
   - maybe Discord, LinkedIn, YouTube, or other relevant homes

4. **Current focus / about section**
   - current projects
   - current learning areas
   - specialties
   - fun facts if useful

5. **Tools and tech**
   - a curated icon row, not a giant kitchen sink

6. **Featured projects**
   - strongest repos, tools, or mod collections
   - ideally with short descriptions or repo cards

7. **Stats section** *(optional)*
   - GitHub Readme Stats card
   - Top Languages card
   - maybe WakaTime if genuinely meaningful

8. **Fun extras** *(optional)*
   - contribution snake
   - painter art
   - themed GIF
   - footer capsule render

### Profile-specific rules we are locking in
- center-align the **hero zone only**
- left-align most real text for readability
- use **one icon family** for social/tool rows
- keep the first screenful clean; no widget soup
- no wall of 20+ badges unless they are serving a clear purpose
- if using animated or decorative elements, limit them so the page still feels polished rather than chaotic

### Good profile extras
- capsule-render header/footer
- a concise YAML-style or bullet-based “about me” block
- repo cards for flagship projects
- themed icons for tools and contact links
- one strong visual gimmick max

### Things to avoid in the profile README
- every widget available on the internet
- giant unstructured paragraphs
- too many colors competing at once
- visual styles that clash
- stats with no context
- novelty features that overpower the actual work

### Starter profile skeleton
```md
<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&height=180&section=header&text=Chris%20Carpenter&fontAlignY=35&fontSize=46&theme=radical" />
</p>

# 👋 Hey, I build weirdly useful things

> **"Space mods, automations, tools, and the occasional gloriously overengineered side quest."**

## 🚀 What I'm Working On
- Space Engineers mods
- n8n automations
- small tools with big opinions

## 🧰 Tools & Tech
[icon row or badges]

## 🌌 Featured Projects
- project one
- project two
- project three

## 📈 GitHub Snapshot
[stats cards here if we decide to use them]
```

---

## Reference Log

These references informed the style decisions above.

| Reference | What it gives us | Practical takeaway | Caution |
|---|---|---|---|
| `https://medium.com/design-bootcamp/how-to-design-an-attractive-github-profile-readme-3618d6c53783` | profile README inspiration | strong header, icon links, YAML-style about section, dynamic visual touches | use for ideas, not copy-paste templating |
| `https://github.com/kyechan99/capsule-render` | dynamic banner/title rendering | use for hero headers and footers on profile or flagship pages | service is best-effort; avoid overuse |
| `https://www.freepik.com/icons` | icon/illustration source | useful when we need themed decorative assets | verify license/attribution and keep style consistent |
| `https://github.com/anuraghazra/github-readme-stats` | stats and repo cards | great for profile README cards and compact portfolio signals | public endpoint can be rate-limited; prefer GitHub Actions/self-hosting if needed |
| `https://github.com/mattrltrent/github_painter` | contribution graph art | optional personality piece for a profile README | use carefully; decorative only |

---

## Quick Decision Table

| Enhancement | Standard public repo README | Flagship / landing README | Profile README |
|---|---|---|---|
| Emoji title + tagline | Yes | Yes | Yes |
| Themed icons | Yes, sparingly | Yes | Yes |
| Capsule-render header | **Yes, by default** | **Required unless there is a strong reason not to** | Recommended |
| Family-specific capsule style | **Yes** | **Yes** | **Yes** |
| Stats cards | Rarely | Maybe | Yes, if curated |
| Contribution art | No | No | Optional only |
| GIFs | Only if informative | Yes, in moderation | Yes, in moderation |
| Footer flourish | Optional | Encouraged | Encouraged |

---

## Writing Rules

### Do
- keep commands, paths, and setup steps exact
- explain what the project does early
- make headings scannable
- use bullets when listing features or files
- preserve real technical detail even when simplifying prose
- add personality in the intro and transitions, not in the critical instructions
- choose visuals that support the project theme
- test assets in both dark and light mode when possible

### Don’t
- remove technical detail for the sake of brevity
- bury important requirements under jokes
- write in a stiff enterprise tone
- overdo the humor
- invent capabilities the project does not actually have
- mix incompatible icon styles
- create a badge wall with no hierarchy
- let decorative widgets become the main content

---

## Starter Template for Normal Public READMEs

```md
# 🚀 Project Name

> **"A short, punchy line that says what this thing does and sounds like a person wrote it."**

Brief intro paragraph explaining what the project is, who it is for, and why it exists.

## 🚀 Quick Start
1. Download or install the project
2. Run the main command or executable
3. Use the primary workflow immediately

## ✨ Features
- Feature one
- Feature two
- Feature three

## 🔧 Usage
Explain how to use the project, run the workflow, install the mod, etc.

## 📁 Project Structure
- `folder/` — what lives here
- `file.ext` — why it matters

## 📝 Notes
Add caveats, compatibility info, or current status.

## 🧡 Support
If the project is free and community-supported, add a short support note and include the standard Patreon button here.

[![Support on Patreon](https://raw.githubusercontent.com/Godimas101/personal-projects/main/patreon/images/buttons/patreon-medium.png)](https://patreon.com/Godimas101)

*Optional closing pun or sign-off.*
```

---

## Source of Truth Examples in This Workspace

When in doubt, mirror the tone and structure of:
- `n8n-projects/the-canadian-space/tcs-workflows/README.md`
- `mods/space-engineers-mods/README.md`
- `toolkits/space-engineers-modders-tool-kit/README.md`

---

## Final Test

Before finishing a public README, check:
- Does it still contain all necessary technical detail?
- Does it sound like a real person wrote it?
- Are the headings and structure easy to scan?
- If visuals are used, do they actually help?
- Are icon choices and colors consistent?
- If support is relevant, is there a clear `## 🧡 Support` section near the bottom?
- Does it still work in GitHub dark and light themes?
- Is the humor light and supportive rather than distracting?

If yes, ship it.
