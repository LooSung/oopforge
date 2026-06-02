# OOPforge

![CI](https://github.com/LooSung/oopforge/actions/workflows/lint.yml/badge.svg)
![Examples](https://github.com/LooSung/oopforge/actions/workflows/examples.yml/badge.svg)
![License](https://img.shields.io/github/license/LooSung/oopforge)

> **AI 负责交付功能，OOPforge 负责守住架构。**
>
> *用 harness engineering 阻止 vibe coding 毁掉你的后端。*

**Forge small. Compose forever.** OOPforge 将 OOP/DDD 定义为代理遵循的方言——技能是语法，hard rules 是 lint，可运行的 `examples/` 是参考实现，install 与命令是运行时。它是方法论包 + agent harness，而非通用 agent framework。

它让 Claude Code、Codex CLI、Cursor 等兼容代理在写代码前，先围绕 **领域模型**、**聚合**、**端口**、**适配器** 与 **可测试用例** 进行设计。

专注 **Java (Spring)** · **Python (FastAPI)** —— **3 层 (Controller/Service/Repository)** 或 **hexagonal/clean** 任选，**OpenAPI/Swagger** 默认开箱即用。

[English](./README.md) · [한국어](./README.ko.md) · [日本語](./README.ja.md) · [中文](./README.zh.md)

---

## 快速开始

### 1. 安装

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/LooSung/oopforge/main/scripts/setup/bootstrap.sh)"
```

### 2. 重启 agent

重启 Claude Code、Codex CLI 或 Cursor Agent CLI 会话以加载 skills 与 commands。

**Cursor:** 显式加载 pack:

```bash
cursor-agent --plugin-dir ~/.oopforge
```

### 3. 运行 Craft

各 harness 的入口都是 **Craft**；**调用方式**不同。

| Harness | 调用 |
|---|---|
| **Claude Code** | `/oopforge:craft <request>` — 斜杠命令 |
| **Codex CLI** | `/skills` → 选 **oopforge**，然后**不要**以 `/` 开头 (Codex 把 `/` 留给内置命令) |
| **Cursor Agent CLI** | `--plugin-dir` 后用自然语言 ([Cursor setup](docs/cursor.md)) |

**Claude Code:**

```text
/oopforge:craft 添加一个 Email 值对象
```

**Codex CLI** (`/skills` → oopforge 之后):

```text
Use OOPforge craft: 添加一个 Email 值对象
```

**Cursor:**

```text
Use OOPforge craft: 添加一个 Email 值对象
```

---

## Advanced Usage

纯咨询类请求时，Craft 只推荐最小路径，不直接实现 (各 harness 相同)。

高级用户可让 Craft 从 Discovery、Design、Delivery Plan、Skeleton、Implement、Test 或 Refactor 等特定 workflow stage 开始。

已安装？见 [Install](#install) 了解手动设置、更新与故障排查。

Harness 指南: [Claude Code](docs/claude-code.md) · [Codex](docs/codex.md) · [Cursor](docs/cursor.md)

---

## 为什么是 OOPforge

OOPforge 是 **DDD / OOP 专用的 AI 工程 pack**，不是通用 agent framework。**OOP 方言语法的 harness 工程** — 技能即语法，硬规则即 lint，`examples/` 即参考实现，install 与命令即运行时。

| 原则 | 含义 |
|---|---|
| **Small** | 一个 skill 一个概念，200 行以内 |
| **Measurable** | 300 行/文件，20 行/方法 |
| **Workflow-first** | Discovery → Test，保留 human checkpoint |
| **Proof over philosophy** | 可运行的 Java/Python 示例 |
| **Domain-first** | domain layer 零 framework import |

简而言之：**让结构成为默认**，避免 God Service。

---

## 如何使用 OOPforge

**新手从这里开始:** **[图书馆借阅指南 →](docs/guides/library-loan/README.zh.md)**  
Discovery → Design → Skeleton → Implement (Java + Python) → Test

指南目录: [EN](docs/guides/library-loan/README.md) · [KO](docs/guides/library-loan/README.ko.md) · [JA](docs/guides/library-loan/README.ja.md) · [ZH](docs/guides/library-loan/README.zh.md)

| 资料 | 用途 |
|---|---|
| [图书馆借阅指南](docs/guides/library-loan/README.zh.md) | 完整工作流教程 |
| [Examples index](examples/README.md) | 可运行证明 — 4 种栈，相同 place-order |
| [order-java](examples/order-java/) · [order-java-layered](examples/order-java-layered/) | Java hexagonal · Java 3-tier |
| [order-python](examples/order-python/) · [order-python-layered](examples/order-python-layered/) | FastAPI clean · FastAPI 3-tier |
| [Discovery 样本 (library)](docs/sample-output/discovery-library.zh.md) | 期望 agent 输出 ([EN](docs/sample-output/discovery-library.md) · [KO](docs/sample-output/discovery-library.ko.md) · [JA](docs/sample-output/discovery-library.ja.md)) |
| [Design 样本 (library)](docs/sample-output/design-library.zh.md) | 期望 agent 输出 ([EN](docs/sample-output/design-library.md) · [KO](docs/sample-output/design-library.ko.md) · [JA](docs/sample-output/design-library.ja.md)) |

每个工作流阶段结束时有 **人工检查点** — 不要跳过。

---

## Philosophy

> **Model is replaceable. Workflow is permanent.**

模型会不断变化：Claude、GPT、OSS，以及之后的新模型。
但 workflow、contracts、architectural discipline 会长期存在。

OOPforge 不是模型层，而是 **development protocol layer**。

### 4 Principles

1. **Small** — 一个 skill 只负责一个 concept，200 行以内。
2. **Clean** — Domain layer 不依赖 framework import。
3. **Composable** — 用小块能力逐步组合。
4. **Sustainable** — 避免 mega prompt，保留 human checkpoint。

---

## Install

### 常用命令 (在 `~/.oopforge` 或本 repo 根目录)

```bash
./scripts/setup/install.sh          # 安装 symlink
./scripts/setup/doctor.sh           # 检查 pack 与链接
./scripts/setup/install.sh update   # git pull 后刷新 symlink
```

### Quick

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/LooSung/oopforge/main/scripts/setup/bootstrap.sh)"
```

### Manual

```bash
git clone https://github.com/LooSung/oopforge ~/.oopforge
cd ~/.oopforge
chmod +x scripts/setup/*.sh
./scripts/setup/install.sh
./scripts/setup/doctor.sh
```

`scripts/setup/install.sh` 会把 OOPforge symlink 到已检测到的 Claude Code / Codex CLI 配置目录。

| Agent | Status | Install target |
|---|---|---|
| **Claude Code** | Supported | `~/.claude/{skills,commands}/oopforge` |
| **Codex CLI** | Supported | `~/.codex/skills/oopforge` |
| **Cursor Agent CLI** | Experimental | `cursor-agent --plugin-dir ~/.oopforge` |
Symlink 安装后，在 `~/.oopforge` 执行 `git pull` 即可更新 skill 内容。需要重建链接时运行 `./scripts/setup/install.sh update`。

### 本地 smoke test

```bash
./scripts/ci/smoke-test.sh
```

---

## Use

### `/oopforge:craft` — 不确定从哪里开始时

```text
/oopforge:craft Add a refund use case to the existing payment domain
/oopforge:craft Fix the bug that allows cancellation after shipment
```

`/oopforge:craft` 会检查请求，并推荐或执行最小的 OOP path。

### Stack 标识符

| Stack | 架构 | 何时使用 |
|---|---|---|
| `java-spring-layered` | 3 层 (Controller/Service/Repository) | 小服务、MVP |
| `java-spring-hexagonal` | Hexagonal | 领域复杂 |
| `python-fastapi-layered` | 3 层 (Router/Service/Repository) | 小服务、MVP |
| `python-fastapi-clean` | Clean | 领域复杂 |

所有 backend skeleton 都 **默认启用 OpenAPI/Swagger UI** (springdoc / FastAPI 内置)。

### Full workflow

```text
/oopforge:craft Start Discovery for the order domain. No code yet.
/oopforge:craft Implement place-order in java-spring-layered
```

也可以直接用自然语言：

> "Build an Order aggregate in Java, following OOPforge rules."

### 记忆库 (跨会话续接)

为了让工作在不同对话间留存，OOPforge 保留一份轻量记忆。写下来，需要时再取出。

- 每个工作项对应一个文档 `.craft/<kind>-<slug>.md` (例如 `.craft/feature-member-management.md`)，记录决策、进度与下一步。
- 回来时 Craft 会**先读取**对应文档，并从那里继续。
- `.craft/` 默认 gitignore (个人笔记)。可在项目 `AGENTS.md` 用 `OOPforge work dir: <path>` 一行更改位置。

详见 [`skills/workflow/continuity.md`](skills/workflow/continuity.md)。

---

## What's inside

```
skills/
├── workflow/        Recommended: Discovery → Design → Delivery Plan → Skeleton → Implement → Test
├── principles/      OOP decision principles
├── playbooks/       Craft task checklists
├── oop/             Domain model + use-case boundary
├── lang/            Backend stack selection (layered vs hexagonal/clean)
└── skeleton/        Backend package structure + empty types

commands/            Claude Code slash command entry point + /oopforge:craft
docs/roadmap.md      方向 · 优先级 · 非目标
AGENTS.md            cross-agent repository instructions
CLAUDE.md            Claude Code bootstrap instructions
scripts/
├── setup/           bootstrap, install, uninstall, doctor
├── ci/              lint-skills, smoke-test
└── path-convention.md
```

---

## Hard Rules

Enforceable measurable rules live in [`AGENTS.md`](./AGENTS.md). This README keeps the user-facing overview.

---

## Roadmap

打包阶段：

- **Phase 1** — Lightweight portable methodology pack (symlinks)
- **Phase 2** — Claude Code / Codex / Cursor plugin marketplaces (Cursor CLI: `--plugin-dir` today; bootstrap symlink + marketplace pending)
- **Phase 3** — Standalone CLI built on Claude Agent SDK

方向、优先级、非目标 (短期/中期/长期、语言扩展、lint 强制、anti-pattern 目录): **[docs/roadmap.md](./docs/roadmap.md)**

---

## Inspiration

- Eric Evans, *Domain-Driven Design*
- Vaughn Vernon, *Implementing Domain-Driven Design*
- Robert C. Martin, *Clean Architecture*
- Kent Beck, *Test-Driven Development: By Example*

---

## Reference

Reference only — packaging and layout ideas, not a dependency.

- Multi-harness plugin structure: [obra/superpowers](https://github.com/obra/superpowers)
- 技能路由与“最小路径”理念: [pstack by Lauren (Cursor)](https://cursor.com/en-US/lp-team/lauren)

---

## License

MIT
