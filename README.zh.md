# OOPforge

> **Forge small. Compose forever.**
>
> 一个面向 AI coding agents 的 OOP/DDD 方法论包，为 Claude Code、Codex CLI、Cursor 等工具注入 clean architecture discipline。

[English](./README.md) · [한국어](./README.ko.md) · [日本語](./README.ja.md) · [中文](./README.zh.md)

---

## 为什么是 OOPforge

OOPforge 是 **DDD / OOP 专用的 AI 工程 pack**，不是通用 agent framework。

| 原则 | 含义 |
|---|---|
| **Small** | 一个 skill 一个概念，200 行以内 |
| **Measurable** | 300 行/文件，20 行/方法 |
| **Workflow-first** | Discovery → Test，保留 human checkpoint |
| **Proof over philosophy** | 可运行的 Java/Python 示例 |
| **Domain-first** | domain layer 零 framework import |

简而言之：**让结构成为默认**，避免 God Service。

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

### Quick

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/LooSung/oopforge/main/bootstrap.sh)"
```

### Manual

```bash
git clone https://github.com/LooSung/oopforge ~/.oopforge
cd ~/.oopforge
chmod +x install.sh uninstall.sh doctor.sh
./install.sh
./doctor.sh
```

`install.sh` 会把 OOPforge symlink 到已检测到的 Claude Code / Codex CLI 配置目录。

| Agent | Status | Install target |
|---|---|---|
| **Claude Code** | Supported | `~/.claude/{skills,agents,commands}/oopforge` |
| **Codex CLI** | Supported | `~/.codex/skills/oopforge` |
| **Cursor** | Not yet (Phase 2) | No installer — manifest only at `.cursor-plugin/` |
| **OpenCode** | Experimental | `INSTALL_OPENCODE=1 ./install.sh` |

Symlink 安装后，在 `~/.oopforge` 执行 `git pull` 即可更新 skill 内容。需要重建链接时运行 `./install.sh update`。

---

## Use

```text
/oopforge:discovery order domain
/oopforge:design place-order use case
/oopforge:skeleton java-spring
/oopforge:implement place-order
```

也可以直接用自然语言：

> "Build an Order aggregate in Java, following OOPforge rules."

---

## What's inside

```
skills/
├── workflow/        Recommended: Discovery → Design → Delivery Plan → Skeleton → Implement → Test
├── oop/             Aggregate Root, Value Object, Domain Event, ...
└── lang/
    ├── java/        Spring hexagonal layout, JPA repository
    └── python/      Pydantic value objects, clean FastAPI layout

agents/              ddd-architect subagent
commands/            Claude Code slash commands for workflow stages
AGENTS.md            cross-agent repository instructions
CLAUDE.md            Claude Code bootstrap instructions
```

---

## Hard Rules

- Domain layer framework imports: **0**
- One file: **≤ 300 lines** — reviewable PR diff size
- One method: **≤ 20 lines preferred** — single responsibility
- One skill file: **≤ 200 lines** — one concept per agent context load
- No public setters; use static factory methods
- Defensive copy collections at boundaries
- No domain logic without tests

---

## Roadmap

- **Phase 1** — Lightweight portable methodology pack (symlinks)
- **Phase 2** — Claude Code / Codex / Cursor plugin marketplaces (Cursor: no ETA; manifest only)
- **Phase 3** — Standalone CLI built on Claude Agent SDK

---

## License

MIT
