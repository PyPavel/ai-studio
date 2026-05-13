# Skills Reference — AI Studio

Each role in the AI Studio uses specific skills. These skills are now **embedded inline** in the prompt templates (`templates/prompts/*.md`), so the template is fully self-contained. You don't need to install any skills separately.

However, if you want to use the **full Hermes skill versions** (with advanced features), install them with:
```bash
hermes skills install <skill-name>
```

---

## Core Roles & Embedded Skills

### Analyst → `templates/prompts/analyst.md`
Embedded methodology from:
- **support-analytics-reporter** — Daily health checks, metrics calculation, actionable reports

### R&D → `templates/prompts/rnd.md`
Embedded methodology from:
- **scientific-brainstorming** — Explore-Question-Propose-Design-Approve cycle
- **hypothesis-generation** — Structured hypothesis with evidence and validation plan

### PM → `templates/prompts/pm.md`
Embedded methodology from:
- **product-manager** — RICE scoring, impact/effort analysis, decision matrix
- **product-sprint-prioritizer** — Prioritization framework for sprint planning
- **brainstorming** — Exploration and approach generation

### Senior Developer → `templates/prompts/senior.md`
Embedded methodology from:
- **subagent-driven-development** — Per-task implementation + two-stage review (spec → quality)
- **verification-before-completion** — Mandatory verification before claiming done

### Junior Developer → `templates/prompts/junior.md`
Embedded methodology from:
- **systematic-debugging** — 4-phase root cause analysis (detect → understand → fix → verify)
- **engineering-sre** — Site reliability practices, monitoring, quick fixes

---

## Optional Skills (for advanced use)

If you want to enhance any role, install these additional skills:

| Skill | Role | Purpose |
|---|---|---|
| `engineering-code-reviewer` | Senior | Advanced code review with security and performance checks |
| `requesting-code-review` | Senior/Junior | Structured code review request templates |
| `finishing-a-development-branch` | Senior | Clean branch completion, merge, PR creation |
| `writing-plans` | Senior | Detailed implementation planning |
| `executing-plans` | Senior | Alternative to subagent-driven-development |
| `marketing-seo-specialist` | R&D/PM | SEO research and optimization |
| `marketing-content-creator` | PM | Content strategy and creation |
| `marketing-growth-hacker` | R&D | Growth experiments and user acquisition |
| `arxiv` | R&D | Academic paper search |
| `paper-lookup` | R&D | Multi-database paper search |
| `database-lookup` | R&D | Scientific data APIs |
| `tradingagents-local-query` | Analyst | Stock analysis (if trading studio) |
| `polars` | Analyst | Fast DataFrame analysis |
| `networkx` | Analyst | Network/graph analysis |

---

## Domain-Specific Skill Combinations

### Trading Studio
```yaml
skills:
  analyst: [support-analytics-reporter, tradingagents-local-query, polars, networkx]
  rnd: [scientific-brainstorming, hypothesis-generation, arxiv, paper-lookup, database-lookup, polymarket, tradingagents-local-query]
  pm: [product-manager, product-sprint-prioritizer, finance-financial-analyst, polymarket]
  senior: [subagent-driven-development, engineering-code-reviewer, verification-before-completion]
  junior: [systematic-debugging, engineering-sre]
```

### Web App Studio
```yaml
skills:
  analyst: [support-analytics-reporter, marketing-daily-news-briefing]
  rnd: [brainstorming, hypothesis-generation, marketing-seo-specialist, marketing-growth-hacker]
  pm: [product-manager, product-sprint-prioritizer, marketing-content-creator]
  senior: [subagent-driven-development, engineering-frontend-developer, engineering-backend-architect, verification-before-completion]
  junior: [systematic-debugging, engineering-sre]
```

### Research Studio
```yaml
skills:
  analyst: [support-analytics-reporter, scientific-critical-thinking, statistical-analysis]
  rnd: [scientific-brainstorming, hypothesis-generation, arxiv, paper-lookup, database-lookup, timesfm-forecasting]
  pm: [product-manager, product-sprint-prioritizer]
  senior: [subagent-driven-development, engineering-data-engineer, verification-before-completion]
  junior: [systematic-debugging, engineering-sre]
```
