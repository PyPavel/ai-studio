# AI Studio Factory

A reusable template for spawning autonomous AI agent teams.

Clone this repo, define your project in `config/studio.yaml`, run `python3 scripts/setup.py`, and your studio is live.

## Quick Start

```bash
# 1. Clone or copy the template
cp -r /home/pavel/tools/ai-studio /home/pavel/tools/my-studio
cd /home/pavel/tools/my-studio

# 2. Edit config with your project
vim config/studio.yaml

# 3. Bootstrap (creates data files + cron jobs)
python3 scripts/setup.py

# 4. Give your first directive
vim data/user_directives.md

# 5. Run PM now to process it
./scripts/trigger.sh pm
```

## Project Structure

```
ai-studio/
├── config/
│   └── studio.yaml              # Project definition (edit this)
├── templates/
│   ├── prompts/                 # Agent role templates
│   │   ├── analyst.md
│   │   ├── rnd.md
│   │   ├── pm.md
│   │   ├── senior.md
│   │   └── junior.md
│   └── data/                    # Data file templates
│       ├── user_directives.md.tpl
│       ├── studio_memory.md.tpl
│       └── product_requirements.md.tpl
├── scripts/
│   ├── setup.py                 # Bootstrap: render templates + create cron jobs
│   ├── trigger.sh               # On-demand: ./trigger.sh pm
│   └── render_prompts.py        # Render a single role prompt
├── SKILLS_REFERENCE.md          # Which skills to use per role and project type
├── data/                        # Created by setup.py (runtime data)
│   ├── user_directives.md       # Write directives here for immediate action
│   ├── studio_memory.md         # Studio state, backlog, rejected ideas
│   ├── product_requirements.md  # APPROVED/NEEDS_DATA/REJECTED tasks
│   └── sprint_results.md        # What Senior implemented this sprint
└── reports/
    └── analyst/                 # Daily reports from Analyst agent
```

## The 5-Agent Pipeline

| Agent | Schedule | Input | Output |
|---|---|---|---|
| **Analyst** | 06:00 | System logs + metrics | `reports/analyst/YYYY-MM-DD_report.md` |
| **R&D** | 07:00 | NEEDS_DATA + research tools | `data/rnd_findings.md` |
| **PM** | 08:00 | R&D findings + Directives + Analyst | `data/product_requirements.md` |
| **Senior** | 10:00 | APPROVED tasks + Directives | `data/sprint_results.md` + Git commits |
| **Junior** | Hourly | System health | Alerts + quick fixes |

**Timeline:** 06:00 → 07:00 → 08:00 → 10:00 → :00 every hour

## Key Features

### Directives Pipeline (Highest Priority)
Write tasks to `data/user_directives.md` at any time. They bypass R&D/Analyst evaluation entirely.

PM auto-APPROVES them → Senior executes FIRST → moved to "Completed Directives".

```markdown
### D-1: Add dark mode toggle
- **Domain:** frontend
- **Description:** Add a dark/light theme toggle to the settings page
- **Acceptance Criteria:** Toggle works, preference persists across sessions
- **Date Added:** 2026-05-13
```

### Zero Backlog Policy
All APPROVED features must be implemented. No exceptions.

### On-Demand Execution
```bash
./scripts/trigger.sh analyst   # Run only analyst
./scripts/trigger.sh pm        # Run only PM
./scripts/trigger.sh senior   # Run only Senior
./scripts/trigger.sh all       # Run full pipeline (not built-in, chain manually)
```

## Roles & Skills Reference

See `SKILLS_REFERENCE.md` for:
- Which skills to use per role and project type
- Core skills (every studio)
- Domain-specific skills (trading, web, research, marketing, etc.)
- Recommended configs for 3 project types

Quick examples:

**Trading Studio** — crypto, stock, forex, polymarket trading
```
analyst: support-analytics-reporter, ai-trader-system-logic, polars, networkx
rnd: scientific-brainstorming, hypothesis-generation, arxiv, paper-lookup, database-lookup, polymarket, tradingagents-local-query
pm: product-manager, product-sprint-prioritizer, finance-financial-analyst, polymarket
senior: subagent-driven-development, engineering-code-reviewer, verification-before-completion
junior: systematic-debugging, engineering-sre
```

**Web App Studio** — frontend + backend + marketing
```
analyst: support-analytics-reporter, marketing-daily-news-briefing
rnd: brainstorming, hypothesis-generation, marketing-seo-specialist, marketing-growth-hacker
pm: product-manager, product-sprint-prioritizer, marketing-content-creator
senior: subagent-driven-development, engineering-frontend-developer, engineering-backend-architect
junior: systematic-debugging, engineering-sre
```

## How to Define Your Project

Edit `config/studio.yaml`:

```yaml
studio:
  name: "My SaaS Studio"
  description: "Autonomous team for building my SaaS product"

project:
  name: "My SaaS"
  description: |
    A B2B SaaS for task management with team collaboration,
    Slack integration, and automated reporting.
  domains:
    - frontend
    - backend_api
    - integrations
    - analytics

health:
  - name: "web-app"
    url: "http://localhost:3000/health"
  - name: "api"
    url: "http://localhost:8080/api/health"

schedule:
  analyst: "0 6 * * *"
  rnd: "0 7 * * *"
  pm: "0 8 * * *"
  senior: "0 10 * * *"
  junior: "0 * * * *"

skills:
  analyst: [support-analytics-reporter]
  rnd: [brainstorming, hypothesis-generation, marketing-seo-specialist, marketing-growth-hacker]
  pm: [product-manager, product-sprint-prioritizer, brainstorming]
  senior: [subagent-driven-development, engineering-code-reviewer, engineering-frontend-developer, engineering-backend-architect, verification-before-completion]
  junior: [systematic-debugging, engineering-sre]
```

## Rules

1. **Use real LLM agents with skills** — never Python script stubs
2. **Communicate via files** — agents pass work through `data/*.md`
3. **Telegram summaries SHORT** — max 3500 chars
4. **Verify before reporting** — check `last_status` before claiming success
5. **Zero Backlog** — all APPROVED features must be implemented
6. **Git mandatory** — Senior commits every feature with conventional commits