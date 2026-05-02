# CHRIS CARPENTER

**Email:** [your.email@example.com]  
**Phone:** [XXX-XXX-XXXX]  
**Location:** Toronto, Ontario, Canada  
**LinkedIn:** https://www.linkedin.com/in/rustygear/  
**Portfolio:** [The Canadian Space](https://thecanadian.space) | [Steam Workshop](https://steamcommunity.com/id/godimas/myworkshopfiles) | [GitHub](https://github.com/Godimas101)

---

## OBJECTIVE

[Placeholder - Customize based on target role and company]

---

## KEY ACCOMPLISHMENTS

**AI-Powered QA Force-Multiplication at Prodigy**
- Built **prodigy-qa-skills** — a complete AI-assisted QA workflow as a suite of 7 Claude Code slash-command skills (6 production, 1 in development). Created solo in response to a company-wide layoff, designed to maintain QA velocity with reduced headcount.
- **The 7 skills:** `/qa-pr-analysis` (PR risk + bug surfacing), `/qa-release-rpg` (find release PR → analyze → create AIO Tests cycles for Stage and Prod → post Slack release summary with threaded squad breakdowns), `/qa-file-bug` (cross-skill bug-filing helper), `/qa-translation-analysis` (pt-BR/es/fr/de/ja against custom Prodigy glossary, autonomous bug filing for misses), `/qa-sentry-analysis` (pull errors/stack traces/breadcrumbs by user or issue ID, classify against known patterns, offer to file), `/qa-test-cases` (read Jira/Confluence/Figma → write structured test cases → import to AIO Tests via API with traceability links), `/qa-feature-context` (in dev — bootstrap a feature folder by pulling epic + child tickets + PRs + Figma + Confluence).
- **Quantified impact:**
  - **Test case writing:** 2–3 days per feature collapsed to ~30 minutes of focused review
  - **PR review + bug filing:** ≥5 hours saved per QAer per week
  - **3 major Prodigy RPG releases** run end-to-end through `/qa-release-rpg`
  - **Several P1 issues caught and stopped** via `/qa-pr-analysis` before they ever reached QA
  - **Localization testing standard:** `/qa-translation-analysis` is now the team's standard process for in-game localization QA
  - **Bug filing fully delegated:** I no longer write bug reports manually. I describe the issue in a few lines; the suite — informed by shared product context — files complete bugs with localization keys, suspected API calls, related server issues, and pattern-matched root cause hypotheses
- **Architectural decisions that scale:**
  - **Multi-product context system** — supports 6 Prodigy products (RPG, Village Builder, Pet Races, Arcadia, Teacher Portal, shared platform); each has its own context files
  - **Index-based routing** — RPG's `rpg-index.md` routes skills to load only the files they need (architecture/risk for PR analysis, release/checklists for releases, overview/zone reference for test cases) — keeps Claude's context window lean
  - **Cross-session journal** — local-only, gitignored, captures in-progress work between Claude Code sessions
  - **Self-staleness awareness** — Repo Library Refresh Tracker flags entries due for refresh and offers to update them
  - **Cross-skill orchestration** — `/qa-file-bug` is a callable subroutine other skills invoke
  - **Production-grade error handling** — 401/403/404 dispatch, OAuth expiry detection, GitHub pagination, MCP tool failure recovery
  - **Symlink-based deployment** — `git pull` is the entire update mechanism, no re-installation
- **Adoption path:** suite is now being introduced to the broader Prodigy QA org via my manager. I am leading the rollout — teaching QAers on Village Builder, Pet Races, and Arcadia how to author the product-specific context files their teams need so the suite scales beyond me.

**QA Test Case Viewer (VS Code Extension)**
- Built a custom VS Code extension that renders the structured JSON + markdown notes prodigy-qa-skills produces into a human-readable, searchable, inline-editable interface — split-view markdown editor with live preview, heading TOC sidebar, in-source search with synced preview highlighting, document undo integration via WorkspaceEdit.
- Closes the loop on the AI workflow for non-technical QA reviewers — lets them proof and tweak generated test cases without ever opening raw JSON.

**Major Project Leadership**
- Leading QA effort for Prodigy RPG localization: creating test plans, managing outsourcers, running bug triage, coordinating cross-department stakeholders, and planning initial public release
- Led 6-person QA team through complex Phaser-to-Pixi game engine migration, transforming inherited struggling project into organized success
- One of only 2 QA selected for Prodigy's Central QA team, led company-wide test management migration (TestRail → AIO Tests)
- Key QA contributor on Prodigy's second-ever game launch, building workflow tools still used company-wide 5+ years later

**Atlassian Excellence**
- Company Atlassian Admin at both Big Viking Games and Prodigy Education (6+ years)
- Created training programs, internal help desk, and automated workflows integrating Jira with Confluence, Git, and Slack
- Established QA best practices and workflow standards used across multiple teams and projects

**Community Impact**
- Built AI-powered aerospace blog with 24/7 automated content pipeline (The Canadian Space)
- Developed Space Engineers mods with 1,335+ active users, self-teaching C# with AI assistance

**Consistent Excellence**
- 15+ years in game industry across mobile, social, indie, AAA, and live service titles
- Top producer of quality bugs, reports, and test documentation throughout career
- Led and mentored multiple QA teams, consistently delivered on tight schedules

---

## TECHNICAL SKILLS

**AI & Automation**
- **AI Orchestration:** Claude (Anthropic) primary, plus Grok (xAI), Qwen, DeepSeek — multi-stage agent workflow design, prompt engineering for production agents, agent verification and pre-return scan patterns
- **Claude Code Skill Development:** Authoring custom slash-command skills; index-based context routing; cross-session journal patterns; cross-skill orchestration; production-grade error handling and graceful degradation; security guardrails (no-paste-tokens-in-chat enforcement, fine-grained PAT model)
- **Integrations leveraged:** Atlassian MCP (Jira, Confluence), Figma MCP, Sentry MCP, GitHub API (gh CLI), AIO Tests REST API, Slack API, WordPress REST API
- **Workflow Automation:** n8n (advanced, self-hosted), Automation for Jira, Automation for Confluence, GitHub Actions
- **Self-Hosting:** Production VPS management on OVH (migrated from DigitalOcean), 24/7 automation systems with weekly automated maintenance

**Atlassian Suite (Expert)**
- **Administration:** Jira Admin, Confluence Admin, company-wide implementations and training
- **Tools:** Jira, Confluence, Jira Service Desk, Atlassian Suite
- **Workflow Design:** Custom workflows, automation rules, cross-tool integrations

**QA & Test Management**
- **Tools:** TestRail, AIO Tests, Zephyr Scale, XRay
- **Testing:** Manual Testing, User Acceptance Testing, Functional Testing, Integration Testing
- **Documentation:** Test plans, test cases, bug reporting, QA standards establishment

**Development & Technical**
- **Programming:** C# (self-taught with AI assistance), TypeScript, XML configuration
- **VS Code Extension Development:** Custom Editor API, webviews, WorkspaceEdit/document undo integration
- **Version Control:** Git, GitHub Actions, pull request automation
- **APIs:** API integration, web scraping, data aggregation (Twitter API, ScraperAPI, Browserless)
- **Platforms:** Mobile games, HTML5, WordPress, game engines (Phaser, Pixi, Space Engineers)

**Design & Legacy Skills**
- Adobe Photoshop, Microsoft Excel, 3D modeling (3D Max), Google Suite
- Level Design, Game Design, Game Balance

---

## PROFESSIONAL EXPERIENCE

### Prodigy Education | Toronto, ON | Feb 2019 - Present

#### Staff Quality Assurance / IC4 - RPG / Atlassian Admin | Feb 2026 - Present
Returned to RPG team with focus on AI-powered QA and automation in lean team environment following company-wide layoff.
- **Built prodigy-qa-skills**, a suite of 7 Claude Code slash-command skills forming a complete AI-assisted QA workflow (PR analysis, bug filing, release cycle setup, localization, Sentry triage, structured test case authoring with AIO Tests import, feature context bundling). See KEY ACCOMPLISHMENTS for impact details and architecture.
- **Leading rollout to broader Prodigy QA org** — teaching QAers on Village Builder, Pet Races, and Arcadia how to author the product-specific context files their teams need so the suite scales beyond me. The suite has been passed to QA leadership and is being introduced company-wide.
- **Built QA Test Case Viewer (VS Code extension)** — companion tool that renders the suite's structured outputs into a human-readable, inline-editable interface for non-technical reviewers (split-view markdown editor, live preview, TOC sidebar, synced search).
- **Leading Prodigy RPG Localization QA:** Creating test plans, managing outsource testing teams, running bug triage, collaborating cross-functionally for project status, and helping plan/manage initial public release.
- **Day-to-day workflow shift:** I no longer file bug reports manually — describe the issue in a few lines, the suite (informed by shared product context) writes the complete report with localization keys, API call hypotheses, and root cause notes. Bug-attached imagery is the one remaining manual step (MCP server limitation).
- Leveraging AI tools (Claude, Grok) and advanced automation (n8n, Automation for Jira, GitHub Actions) to handle workloads previously requiring larger teams.

**Skills:** Claude Code Skill Development • AI Orchestration • Atlassian Admin (Jira, Confluence) • n8n • AIO Tests REST API • GitHub API • Sentry MCP • Figma MCP • Slack API • Automation for Jira • Localization QA • VS Code Extension Development • TypeScript

#### Central QA / Atlassian Admin | Oct 2025 - Feb 2026
Selected as one of only two QA for elite Central QA team supporting company-wide initiatives.
- Led company-wide test management tool migration from TestRail to AIO Tests through comprehensive analysis and implementation
- Supported multiple game squads with Jira/Confluence setups, workflow changes, and automation implementations
- Led 6-person outsource testing team to tackle large-scale projects beyond internal team capacity
- Pioneered AI tool integration into QA workflow: Claude and Grok for writing tasks, automated playtest documentation
- Built advanced automation: release note generation, Jira ticket automation based on pull request status, workflow tools using Automation for Jira/Confluence and GitHub Actions

**Skills:** Atlassian Admin • TestRail • AIO Tests • AI Integration • Workflow Automation • n8n • Outsourcer Management

#### Quality Assurance III - RPG / Atlassian Admin | Nov 2024 - Oct 2025
Rejoined RPG team working on core combat systems with continued Atlassian administration responsibilities
- Streamlined and automated workflows for multiple RPG teams
- Onboarded new QA hires, and mentored one from a contractor to a full time employee, all the way through to them getting a promotion!

**Skills:** Atlassian Admin • Automation for Jira • TestRail • Workflow Automation • Mobile Game Development

#### Quality Assurance II/III / Atlassian Admin - Village Builder | Apr 2021 - Nov 2024
Key QA role on Prodigy's second-ever game launch with extensive workflow automation responsibilities.
- Built complete QA workflow and automation tools from ground up for new game title
- Created automated workflow tools integrating Jira with Confluence, Git, and Slack - tools still used company-wide today
- Led QA effort on multiple major features including game's multiplayer system implementation
- Established QA best practices for bug filing and documentation that became team standards
- Founded internal Jira help desk for company support tickets, evolving from side project to critical company function

**Skills:** Jira • Confluence • Workflow Automation • Atlassian Admin • Manual Testing • TestRail • Automation for Jira

#### QA Engineer - RPG | Feb 2020 - Nov 2024  
First experience with true live service product, including leadership on major engine migration project.
- **Led major game engine migration** (Phaser → Pixi): Inherited struggling project from another team, reorganized and coordinated 6 internal testers to completion
- Built workflow pipeline for developers and created project management system for easy status tracking
- Worked on RPG game's PVP backend improvements
- Gained extensive live service QA experience in fast-paced environment

**Skills:** Jira • Confluence • Workflow Automation • Manual Testing • UAT • Functional Testing • Integration Testing

### Big Viking Games | London/Toronto, ON | Oct 2013 - Feb 2019

#### Sr. QA Analyst | Toronto | Jul 2016 - Feb 2019
- Lead QA on Facebook Messenger game Galatron using new platform technology
- Build master: handled all merging and deploying across various servers

#### Associate Producer | London, ON | Jul 2015 - Jul 2016
- Managed two separate teams on different projects across two cities
- Established process foundations for growing studio using Atlassian and Google-centric workflows
- Teams developed HTML5 games with agile methodologies

#### Game Designer | London, ON | Jan 2015 - Jul 2015
- Designed and balanced content for Super Spin Slots and Tiny Kingdoms
- Created game design documents and content spreadsheets
- Built design tools and calculators for initial design and post-launch support

#### Quality Assurance Team Lead | London, ON | Oct 2013 - Sep 2015
- **Introduced Jira and DevSuite to Big Viking Games**, setting up multiple teams on Atlassian tools
- Established company-wide QA standards for bug creation and build organization
- QA Team Lead and Community Manager for Tiny Kingdoms project
- Set up agile planning workflows and best practices used across multiple projects
- Onboarded and trained new hires to deliver quality bug reports

### Ubisoft Toronto | Toronto, ON | Oct 2012 - Aug 2013

#### Quality Control Tester
AAA game testing on Splinter Cell: Blacklist (Metacritic 82-84).
- Focused on multiplayer (COOP and PVP) testing for high-profile AAA title
- Consistently top bug producer on multiplayer team while maintaining ticket quality
- Collaborated with international QA teams daily
- Delivered clear, concise, complete bug documentation under demanding deadlines

### Social Game Universe | Toronto, ON | Nov 2011 - Jun 2012

#### Game Designer / QA Tester
- Completed internship, hired as sole game designer for studio
- Designed two titles from ground up, balanced multiple social games
- Led design discussions, brainstorming sessions with developers and artists
- Created game pitches, prototypes, design documents, and content spreadsheets

---

## PERSONAL PROJECTS

### The Canadian Space - AI-Powered Aerospace News Blog
**Founder & Content Automation Engineer | Oct 2025 - Present**  
**URL:** https://thecanadian.space

Fully automated aerospace news blog demonstrating production-level AI orchestration and workflow automation.

**Technical Stack:**
- n8n workflow automation (self-hosted Digital Ocean VPS running 24/7)
- AI orchestration: Claude (workflow design), Qwen/DeepSeek (content generation), Grok (social media)
- Multi-source data aggregation: Twitter API, Spaceflight News API, Launch Library 2, web scrapers
- Automated multi-platform publishing: WordPress, Facebook, Instagram

**Achievements:**
- Built production automation pipeline handling daily content generation with minimal human intervention
- Mastered n8n through hands-on deployment of complex, multi-stage workflows
- Demonstrated AI force-multiplication: solo operation producing work of entire content team
- Self-hosted and maintained production infrastructure

**Content Output:** Daily broadcasts, weekly spotlights, monthly deep-dives

### Space Engineers Game Modding
**Independent Mod Developer | 2023 - Present**  
**Steam Workshop:** https://steamcommunity.com/id/godimas/myworkshopfiles

Self-taught C# game development with AI assistance (Claude Code), creating mods for Space Engineers.

**Portfolio:** 21+ published mods, flagship mod with 1,335+ active subscribers, 3,610+ unique visitors, 101 favorites

**Featured Project: InfoLCD - Apex Update**  
Comprehensive LCD information display system providing real-time ship/station monitoring without programming blocks.
- Client-side C# development using Space Engineers game engine API
- 20+ specialized display apps (inventory, production, systems, safety monitoring)
- XML configuration and mod compatibility system
- Active community engagement with ongoing feature development

**Skills Demonstrated:** C# programming (self-taught), game engine APIs, XML configuration, UI development, version control, community management, AI-assisted learning

---

## EDUCATION

**Video Game Design**  
International Academy of Design and Technology | Toronto, ON | 2004 - 2006  
Graduated with Honors | Focus: 3D modeling, rigging, and animation

**Crafts and Design**  
Sheridan College | Oakville, ON | 2003 - 2004  
Major: Glass with focus on cold shop | Also studied glassblowing and furniture making

**Art Fundamentals**  
Sheridan College | Oakville, ON | 2002 - 2003  
High marks in all classes | Focus: Life drawing, sculpting, and drafting

---

## GAME CREDITS

**Prodigy Education**
- Prodigy RPG - Staff QA Analyst
- Prodigy Village Builder - Sr QA Analyst

**Big Viking Games**
- Fish World - Sr QA Analyst
- Fish World: Match 3 - Sr QA Analyst
- Thor (Game Engine) - Sr QA Analyst
- TAP:R - Sr QA Analyst
- Galatron - QA Team Lead
- Tiny Tappers - QA Team Lead
- GalatronVS - Associate Producer
- Tiny Tappers - Associate Producer
- Yoworld Mobile Companion - Associate Producer
- Super Spin Slots - Game Designer/Associate Producer
- Tiny Kingdoms Adventures - Game Designer/Lead Tester
- Tiny Kingdoms - QA Analyst
- YoWorld - QA Analyst
- Monsters And Dungeons - QA Analyst

**Ubisoft Toronto**
- Splinter Cell: BlackList - Multiplayer Tester

**Social Game Universe**
- Angry Tower Bases - Game Designer
- Dirty Dancing Social Resort - Game Designer

**Groove Games**
- SK Warpath - QA Analyst
- SK LA Street Racing - QA Analyst
- Skill Grounds - QA Analyst
- LA Street Racing - QA Analyst

**3Tone Entertainment**
- Terra Builder: Moon - Modeler/Animator

---

**References available upon request**
