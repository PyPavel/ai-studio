# AI Studio Factory

用于生成自主 AI 代理团队的可重用模板。

克隆此仓库，在 `config/studio.yaml` 中定义您的项目，运行 `python3 scripts/setup.py`，您的工作室即可上线。

## 快速入门

```bash
# 1. 克隆或复制模板
cp -r /home/pavel/tools/ai-studio /home/pavel/tools/my-studio
cd /home/pavel/tools/my-studio

# 2. 使用您的项目信息编辑配置
vim config/studio.yaml

# 3. 引导启动（创建数据文件 + cron 任务）
python3 scripts/setup.py

# 4. 发布您的第一条指令
vim data/user_directives.md

# 5. 立即运行 PM 以处理指令
./scripts/trigger.sh pm
```

## 项目结构

```
ai-studio/
├── config/
│   └── studio.yaml              # 项目定义（编辑此处）
├── templates/
│   ├── prompts/                 # 代理角色模板
│   │   ├── analyst.md
│   │   ├── rnd.md
│   │   ├── pm.md
│   │   ├── senior.md
│   │   └── junior.md
│   └── data/                    # 数据文件模板
│       ├── user_directives.md.tpl
│       ├── studio_memory.md.tpl
│       └── product_requirements.md.tpl
├── scripts/
│   ├── setup.py                 # 引导：渲染模板 + 创建 cron 任务
│   ├── trigger.sh               # 按需运行：./trigger.sh pm
│   └── render_prompts.py        # 渲染单个角色提示词
├── SKILLS_REFERENCE.md          # 每个角色和项目类型使用的技能参考
├── data/                        # 由 setup.py 创建（运行时数据）
│   ├── user_directives.md       # 在此写入指令以立即执行
│   ├── studio_memory.md         # 工作室状态、积压工作、被拒绝的想法
│   ├── product_requirements.md  # 已批准/需要数据/被拒绝的任务
│   └── sprint_results.md        # 高级开发人员在本冲刺中实现的内容
└── reports/
    └── analyst/                 # 分析师代理的每日报告
```

## 5 代理工作流

| 代理 | 时间表 | 输入 | 输出 |
|---|---|---|---|
| **分析师 (Analyst)** | 06:00 | 系统日志 + 指标 | `reports/analyst/YYYY-MM-DD_report.md` |
| **研发 (R&D)** | 07:00 | 需要的数据 + 研究工具 | `data/rnd_findings.md` |
| **产品经理 (PM)** | 08:00 | 研发发现 + 指令 + 分析师 | `data/product_requirements.md` |
| **高级开发 (Senior)** | 10:00 | 已批准任务 + 指令 | `data/sprint_results.md` + Git 提交 |
| **初级开发 (Junior)** | 每小时 | 系统健康状况 | 警报 + 快速修复 |

**时间轴：** 06:00 → 07:00 → 08:00 → 10:00 → 每小时整点

## 核心特性

### 指令流水线 (Directives Pipeline - 最高优先级)
随时将任务写入 `data/user_directives.md`。它们会完全绕过研发/分析师的评估。

PM 会自动批准它们 → 高级开发人员首先执行 → 移动到“已完成指令”。

```markdown
### D-1: 添加深色模式切换
- **领域 (Domain):** 前端
- **描述:** 为设置页面添加深色/浅色主题切换
- **验收标准:** 切换正常工作，偏好在会话间持久化
- **添加日期:** 2026-05-13
```

### 零积压政策 (Zero Backlog Policy)
所有已批准 (APPROVED) 的功能都必须实现。没有例外。

### 按需执行
```bash
./scripts/trigger.sh analyst   # 仅运行分析师
./scripts/trigger.sh pm        # 仅运行产品经理
./scripts/trigger.sh senior    # 仅运行高级开发
./scripts/trigger.sh all       # 运行完整流水线（非内置，需手动串联）
```

## 角色与技能参考

请参阅 `SKILLS_REFERENCE.md` 了解：
- 每个角色和项目类型使用的技能
- 核心技能（每个工作室都需要）
- 特定领域技能（交易、Web、研究、营销等）
- 3 种项目类型的推荐配置

快速示例：

**交易工作室 (Trading Studio)** — 加密货币、股票、外汇、Polymarket 交易
```
analyst: support-analytics-reporter, ai-trader-system-logic, polars, networkx
rnd: scientific-brainstorming, hypothesis-generation, arxiv, paper-lookup, database-lookup, polymarket, tradingagents-local-query
pm: product-manager, product-sprint-prioritizer, finance-financial-analyst, polymarket
senior: subagent-driven-development, engineering-code-reviewer, verification-before-completion
junior: systematic-debugging, engineering-sre
```

**Web 应用工作室 (Web App Studio)** — 前端 + 后端 + 营销
```
analyst: support-analytics-reporter, marketing-daily-news-briefing
rnd: brainstorming, hypothesis-generation, marketing-seo-specialist, marketing-growth-hacker
pm: product-manager, product-sprint-prioritizer, marketing-content-creator
senior: subagent-driven-development, engineering-frontend-developer, engineering-backend-architect
junior: systematic-debugging, engineering-sre
```

## 如何定义您的项目

编辑 `config/studio.yaml`:

```yaml
studio:
  name: "我的 SaaS 工作室"
  description: "用于构建我的 SaaS 产品的自主团队"

project:
  name: "我的 SaaS"
  description: |
    一个包含团队协作、Slack 集成和自动报告功能的
    B2B 任务管理 SaaS。
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

## 规则

1. **使用真实的具备技能的 LLM 代理** — 绝不使用 Python 脚本存根
2. **通过文件通信** — 代理通过 `data/*.md` 传递工作
3. **Telegram 摘要简短** — 最多 3500 字符
4. **报告前验证** — 在声称成功前检查 `last_status`
5. **零积压 (Zero Backlog)** — 所有已批准的功能必须实现
6. **Git 是强制性的** — 高级开发人员使用约定式提交 (conventional commits) 提交每个功能
