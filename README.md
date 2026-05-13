# AI Studio Factory

A reusable template for spawning autonomous AI agent teams (Analyst -> R&D -> PM -> Senior -> Junior).

Clone this repo, define your project in `config/studio.yaml`, run `./scripts/setup.sh`, and your studio is live.

## Quick Start

```bash
git clone <repo-url> /home/pavel/tools/my-project-studio
cd /home/pavel/tools/my-project-studio

# 1. Define your project
vim config/studio.yaml

# 2. Bootstrap the studio
./scripts/setup.sh

# 3. Trigger on demand
./scripts/trigger.sh pm    # Run PM agent now
./scripts/trigger.sh all   # Run full pipeline now
```

## Project Structure

```
.
├── config/
│   └── studio.yaml              # Your project definition
├── templates/
│   ├── prompts/                 # Role prompt templates
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
│   ├── setup.sh                 # One-time bootstrap
│   ├── trigger.sh               # On-demand execution
│   └── render_prompts.py        # Renders templates with config
├── data/                        # Runtime data (created by setup)
│   ├── user_directives.md
│   ├── studio_memory.md
│   ├── product_requirements.md
│   └── sprint_results.md
└── reports/                     # Generated reports
    └── analyst/
```

## How It Works

### The 5-Agent Pipeline
| Agent | Schedule | Input | Output |
|---|---|---|---|
| **Analyst** | 06:00 | System logs + metrics | `reports/analyst/YYYY-MM-DD_report.md` |
| **R&D** | 07:00 | Previous NEEDS_DATA + research tools | `data/rnd_findings.md` |
| **PM** | 08:00 | R&D findings + Analyst report + Directives | `data/product_requirements.md` |
| **Senior** | 10:00 | APPROVED tasks + Directives | `data/sprint_results.md` |
| **Junior** | Every hour | System health | Status alerts + quick fixes |

### Key Features

**Directives Pipeline** — You can write tasks directly to `data/user_directives.md` at any time. These bypass normal evaluation and are executed FIRST by the Senior agent.

**Zero Backlog Policy** — All APPROVED features must be implemented. No exceptions.

**On-Demand Trigger** — Run any agent manually with `./scripts/trigger.sh <agent>`.

## Customizing

Edit `config/studio.yaml` to define:
- Project name and description
- Domains (what your app/system manages)
- Schedule offsets
- Skills per role
- Health check endpoints

The setup script reads this config and creates cron jobs automatically.

## Example Projects

- **Trading Studio** — 4 traders (crypto, stock, forex, poly) with portfolios
- **SaaS Builder** — Frontend + backend + marketing automation
- **Content Factory** — YouTube scripts, thumbnails, scheduling
- **Research Lab** — Paper analysis, hypothesis testing, report generation

## Rules

1. **Use real LLM agents with skills** — never Python script stubs
2. **Communicate via files** — agents pass work through `data/*.md`
3. **Telegram summaries must be SHORT** (<3500 chars)
4. **Verify before reporting** — always check `last_status` before claiming success
5. **Zero Backlog** — all APPROVED features must be implemented
6. **Git mandatory** — Senior commits every feature with conventional commits
