# AI Studio — Skills Reference

This document maps Hermes skills to studio roles and project types.
Use it to choose the right skills for your `config/studio.yaml`.

## How Skills Work in Studios

1. Skills are listed in `config/studio.yaml` under `skills.<role>`.
2. When a cron job runs, Hermes loads these skills automatically.
3. Each skill contains instructions, pitfalls, and workflows the agent follows.
4. **Only load skills relevant to your project** — extra skills waste tokens.

## Core Studio Skills (Every Studio)

These skills apply to ANY project type:

| Skill | Best For | Description |
|---|---|---|
| `support-analytics-reporter` | Analyst | Calculate metrics, analyze logs, generate reports |
| `product-manager` | PM | RICE/ROI analysis, prioritization, backlog management |
| `product-sprint-prioritizer` | PM | Sprint planning, task ordering |
| `subagent-driven-development` | Senior | Spawning and managing developer subagents |
| `engineering-code-reviewer` | Senior | Code review before merging |
| `requesting-code-review` | Senior/Junior | Pre-commit review workflow |
| `verification-before-completion` | Senior/Junior | Verify work before reporting success |
| `systematic-debugging` | Junior | Root cause debugging for fixes |
| `engineering-sre` | Junior | Site reliability, health checks, incident response |
| `brainstorming` | R&D/PM | Structured ideation before building |

## Domain-Specific Skills

### Web Applications
| Skill | Role | Description |
|---|---|---|
| `engineering-frontend-developer` | Senior | React/Vue/Angular, UI implementation |
| `engineering-backend-architect` | Senior | API design, database schema, server architecture |
| `engineering-solidity-smart-contract-engineer` | Senior | Web3/blockchain apps |
| `engineering-minimal-change-engineer` | Senior | Surgical changes only |
| `testing-accessibility-auditor` | Senior | WCAG compliance testing |
| `testing-api-tester` | Senior | API endpoint testing |

### Trading & Finance
| Skill | Role | Description |
|---|---|---|
| `ai-trader-system-logic` | All | Trading studio architecture knowledge |
| `tradingagents-local-query` | R&D/PM | Stock analysis via TradingAgents |
| `polymarket` | R&D/PM | Prediction market screening |
| `finance-investment-researcher` | R&D | Fundamental analysis |
| `finance-financial-analyst` | PM | Financial metrics analysis |
| `statistical-analysis` | R&D | Hypothesis testing, backtesting |
| `polars` | R&D/Analyst | Fast DataFrame operations |
| `networkx` | R&D | Cross-asset correlation analysis |

### Research & Science
| Skill | Role | Description |
|---|---|---|
| `scientific-brainstorming` | R&D | Open-ended research ideation |
| `hypothesis-generation` | R&D | Structured hypothesis formulation |
| `arxiv` | R&D | Academic paper search |
| `paper-lookup` | R&D | 10 paper databases via REST |
| `database-lookup` | R&D | 78 public databases (FRED, SEC, etc.) |
| `scientific-critical-thinking` | R&D | Evidence quality evaluation |
| `timesfm-forecasting` | R&D | Time-series predictions |
| `usfiscaldata` | R&D | US Treasury fiscal data |

### Marketing & Growth
| Skill | Role | Description |
|---|---|---|
| `marketing-seo-specialist` | R&D | SEO optimization, keyword research |
| `marketing-content-creator` | R&D/PM | Content strategy and creation |
| `marketing-growth-hacker` | R&D | Low-cost acquisition experiments |
| `marketing-daily-news-briefing` | Analyst | News collection and summarization |
| `marketing-social-media-strategist` | R&D | Social platform strategy |
| `finance-fraud-detector` | Analyst | Fraud detection in transactions |

### DevOps & Infrastructure
| Skill | Role | Description |
|---|---|---|
| `engineering-devops-automator` | Senior/Junior | CI/CD, cloud infrastructure |
| `engineering-git-workflow-master` | Senior | Branch strategies, conventional commits |
| `testing-performance-benchmarker` | Senior | Load testing, capacity planning |
| `9router` | Junior | AI gateway management |

## Anti-Patterns (Do NOT Load These Together)

- `polymarket` + `tradingagents-local-query` for non-trading projects — waste of tokens
- `scientific-brainstorming` for simple web apps — overkill, use `brainstorming` instead
- Loading 20+ skills per agent — keep it under 8-10 for most roles

## Recommended Role Configs by Project Type

### Trading Studio (Current)
```yaml
skills:
  analyst: [support-analytics-reporter, ai-trader-system-logic, polars, networkx]
  rnd: [scientific-brainstorming, hypothesis-generation, arxiv, paper-lookup, database-lookup, polymarket, tradingagents-local-query, statistical-analysis, finance-investment-researcher, polars, networkx, usfiscaldata]
  pm: [product-manager, product-sprint-prioritizer, finance-financial-analyst, polymarket, tradingagents-local-query, hypothesis-generation, brainstorming]
  senior: [subagent-driven-development, engineering-code-reviewer, requesting-code-review, ai-trader-system-logic, verification-before-completion]
  junior: [ai-trader-system-logic, systematic-debugging, requesting-code-review, engineering-sre]
```

### Web Application Studio
```yaml
skills:
  analyst: [support-analytics-reporter, marketing-daily-news-briefing, polars]
  rnd: [brainstorming, hypothesis-generation, marketing-seo-specialist, marketing-content-creator, marketing-growth-hacker]
  pm: [product-manager, product-sprint-prioritizer, brainstorming]
  senior: [subagent-driven-development, engineering-code-reviewer, requesting-code-review, engineering-frontend-developer, engineering-backend-architect, verification-before-completion]
  junior: [systematic-debugging, requesting-code-review, engineering-sre]
```

### Research Lab Studio
```yaml
skills:
  analyst: [support-analytics-reporter, polars]
  rnd: [scientific-brainstorming, hypothesis-generation, arxiv, paper-lookup, database-lookup, scientific-critical-thinking, statistical-analysis, timesfm-forecasting]
  pm: [product-manager, product-sprint-prioritizer, brainstorming]
  senior: [subagent-driven-development, engineering-code-reviewer, requesting-code-review, verification-before-completion]
  junior: [systematic-debugging, engineering-sre]
```
