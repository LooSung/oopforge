# OOPforge

> **Forge small. Compose forever.**
>
> An OOP/DDD methodology pack that injects clean-architecture discipline into AI coding agents — Claude Code, Codex CLI, Cursor, and friends.

[English](./README.md) · [한국어](./README.ko.md) · [日本語](./README.ja.md) · [中文](./README.zh.md)

---

## Why OOPforge — what's different

Great general-purpose workflow packs already exist ([obra/superpowers](https://github.com/obra/superpowers), [SuperClaude](https://github.com/SuperClaude-Org/SuperClaude_Framework)). OOPforge **complements** them, not competes:

| | obra/superpowers | SuperClaude | **OOPforge** |
|---|---|---|---|
| **Focus** | Workflow · TDD | Full platform · slash commands | **DDD · Hexagonal · OOP domain modeling** |
| **Language** | General | General | **Java + Python (dual-handed)** |
| **UI Language** | EN | EN, ZH, JA | **EN-first + KO/JA/ZH** |
| **Rules** | Guidelines | Behavioral modes | **Concrete metrics (300-line, single-purpose)** |

In short: **A `superpowers` for developers who take DDD seriously.**
Install alongside other packs without conflict.

---

## Philosophy

> **Model is replaceable. Workflow is permanent.**

Models change — Claude, GPT, Gemini, OSS, whatever comes next.
But workflow, contracts, and architectural discipline endure.

OOPforge is not a model layer. It's a **development protocol layer**.

### 4 Principles

1. **Small** — One concept per skill. Under 200 lines.
2. **Clean** — Domain layer free of framework imports. Comments explain "why" only.
3. **Composable** — Tiny pieces assembled over time.
4. **Sustainable** — No mega-prompts. Human checkpoints preserved.

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

The installer symlinks the pack into every detected agent's config directory:
- Claude Code → `~/.claude/{skills,agents,commands}/oopforge`
- Codex CLI → `~/.codex/skills/oopforge`
- Cursor → `.cursor-plugin/` manifest is prepared for Phase 2 marketplace packaging
- OpenCode → experimental, disabled by default; opt in with `INSTALL_OPENCODE=1 ./install.sh`

Edit once in `~/.oopforge`, every agent sees it immediately.

---

## Use

```text
/oopforge:discovery order domain
/oopforge:design place-order use case
/oopforge:skeleton java-spring
/oopforge:implement place-order
```

Or just chat:
> "Build an Order aggregate in Java, following OOPforge rules."

---

## What's inside

```
skills/
├── workflow/        Discovery → Design → Skeleton → Implement (4-stage)
├── oop/             Language-agnostic patterns
│                    aggregate-root, value-object, application-service,
│                    repository-port, domain-event, bounded-context,
│                    factory-method, specification-pattern
└── lang/
    ├── java/        Spring hexagonal layout, JPA repository
    └── python/      Pydantic value objects, clean FastAPI layout

agents/              ddd-architect subagent
commands/            slash commands for each workflow stage
```

---

## Hard Rules (measurable metrics)

- Domain layer framework imports: **0**
- One file: **≤ 300 lines**
- One method: **≤ 20 lines preferred**
- One skill file: **≤ 200 lines**
- Public methods named as use-case verbs (no CRUD names)
- No public setters; use static factory methods
- Defensive copy collections at boundaries
- No domain logic without tests

---

## Roadmap

- **Phase 1 (now)** — Lightweight portable methodology pack (symlinks)
- **Phase 2** — Claude Code / Codex / Cursor plugin marketplaces
- **Phase 3** — Standalone CLI built on Claude Agent SDK

---

## Inspiration

- [obra/superpowers](https://github.com/obra/superpowers) — Multi-harness plugin structure
- [SuperClaude Framework](https://github.com/SuperClaude-Org/SuperClaude_Framework) — Full platform approach
- Eric Evans, *Domain-Driven Design*
- Vaughn Vernon, *Implementing DDD*
- Robert C. Martin, *Clean Architecture*

---

## License

MIT
