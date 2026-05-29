# OOPforge

> **Forge small. Compose forever.**
>
> *A portable OOP/DDD methodology pack for AI coding agents.*

OOPforge gives Claude Code, Codex CLI, Cursor, and compatible coding agents a clear way to model software with **DDD**, **hexagonal architecture**, and **clean domain boundaries**.

[English](./README.md) · [한국어](./README.ko.md) · [日本語](./README.ja.md) · [中文](./README.zh.md)

---

## **Quickstart**

Install OOPforge into the agents detected on your machine:

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/LooSung/oopforge/main/bootstrap.sh)"
```

Then restart your coding agent and ask:

```text
Build an Order aggregate in Java, following OOPforge rules.
```

For Claude Code slash commands:

```text
/oopforge:discovery order domain
/oopforge:design place-order use case
/oopforge:delivery-plan place-order
/oopforge:skeleton java-spring
/oopforge:implement place-order
/oopforge:test place-order
```

---

## **Why OOPforge**

General-purpose methodology packs already exist. OOPforge is narrower on purpose: it focuses on **object-oriented domain modeling** for teams that care about long-lived architecture.

| | obra/superpowers | SuperClaude | **OOPforge** |
|---|---|---|---|
| **Focus** | Workflow · TDD | Full platform · slash commands | **DDD · Hexagonal · OOP domain modeling** |
| **Scope** | General | General | **Domain modeling discipline** |
| **Languages** | General | General | **Java + Python first** |
| **Rules** | Guidelines | Behavioral modes | **Concrete metrics and boundaries** |

In short: **OOPforge is a DDD-focused companion pack**, not a replacement for broader workflow systems.

---

## **Installation**

### **Automatic**

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/LooSung/oopforge/main/bootstrap.sh)"
```

### **Manual**

```bash
git clone https://github.com/LooSung/oopforge ~/.oopforge
cd ~/.oopforge
chmod +x install.sh uninstall.sh doctor.sh
./install.sh
./doctor.sh
```

### **What gets installed**

`install.sh` symlinks OOPforge into supported agent config directories:

| Agent | Status | Install target |
|---|---|---|
| **Claude Code** | Supported | `~/.claude/{skills,agents,commands}/oopforge` |
| **Codex CLI** | Supported | `~/.codex/skills/oopforge` |
| **Cursor** | Prepared | `.cursor-plugin/` manifest for Phase 2 |
| **OpenCode** | Experimental | `INSTALL_OPENCODE=1 ./install.sh` |

Because the install uses symlinks, editing `~/.oopforge` updates every linked agent immediately.

---

## **The Basic Workflow**

OOPforge uses a small delivery loop. *Do not merge planning, implementation, and verification.*

### **Recommended order**

For a new domain or feature, use OOPforge in this order:

```text
Discovery → Design → Delivery Plan → Skeleton → Implement → Test
```

This keeps the agent from jumping into code before the domain language, boundaries, contracts, and verification plan are clear.

| Stage | Output | Do not do |
|---|---|---|
| **1. Discovery** | Glossary, bounded contexts, actors, open questions | Code |
| **2. Design** | Use-case signatures, aggregate outlines, ports | Implementation |
| **3. Delivery Plan** | Scope, contract, implementation order, test/release plan | Coding |
| **4. Skeleton** | Packages, interfaces, empty classes | Business logic |
| **5. Implement** | One use case at a time | Multiple use cases at once |
| **6. Test** | Unit, integration, E2E checks | Untested domain logic |

Each stage ends with a human checkpoint before moving on.

### **Command flow**

```text
/oopforge:discovery payment domain
/oopforge:design approve-payment use case
/oopforge:delivery-plan approve-payment
/oopforge:skeleton java-spring
/oopforge:implement approve-payment
/oopforge:test approve-payment
```

### **Where to start**

- Start at **Discovery** for a new domain or unclear feature.
- Start at **Delivery Plan** if Discovery/Design already exist.
- Start at **Implement** only when the contract and skeleton are already clear.
- Use **Test** whenever you need TDD, regression coverage, or E2E verification.
- Use **Refactor** separately when behavior must stay the same.

**Refactor is intentionally outside the default feature flow.** Use it for existing or imported code that needs cleanup without behavior changes.

### **Single-step commands**

```text
/oopforge:delivery-plan payment approval
/oopforge:test place-order
/oopforge:refactor imported billing module
```

Natural language works too:

```text
Use OOPforge to create a delivery plan for payment approval.
Use OOPforge test workflow to add unit and E2E coverage for place-order.
Use OOPforge refactor workflow to clean up this imported module without changing behavior.
```

---

## **What's Inside**

```text
oopforge/
├── skills/
│   ├── workflow/        Discovery → Design → Delivery Plan → Skeleton
│   │                    → Implement → Test, plus Refactor
│   ├── oop/             Aggregate Root, Value Object, Repository Port,
│   │                    Domain Event, Bounded Context, Factory Method,
│   │                    Specification Pattern
│   └── lang/
│       ├── java/        Spring hexagonal layout, JPA repository
│       └── python/      Pydantic value objects, clean FastAPI layout
├── agents/              ddd-architect subagent
├── commands/            Claude Code slash commands for workflow stages
├── AGENTS.md            cross-agent repository instructions
├── CLAUDE.md            Claude Code bootstrap instructions
├── bootstrap.sh         one-line installer
├── doctor.sh            installation checker
├── install.sh           symlink installer
└── uninstall.sh         symlink remover
```

### **Agent instruction files**

- **`AGENTS.md`** is the shared source of truth for Codex, Cursor, OpenCode, and other compatible agents.
- **`CLAUDE.md`** is a thin Claude Code entry point that imports `AGENTS.md`.

---

## **Hard Rules**

These are intentionally measurable:

- Domain layer framework imports: **0**
- One file: **300 lines or less**
- One method: **20 lines preferred**
- One skill file: **200 lines or less**
- Public methods use **use-case verbs**, not CRUD names
- No public setters; use **factory methods** and intention-revealing behavior
- Collections crossing boundaries are defensively copied or immutable
- Other aggregates are referenced by **ID only**
- No domain logic without tests
- Comments explain *why*; names explain *what*

---

## **Philosophy**

> **Model is replaceable. Workflow is permanent.**

Models change: Claude, GPT, OSS, and whatever comes next.
But *workflow*, *contracts*, and *architectural discipline* last longer.

OOPforge is not a model layer. It is a **development protocol layer**.

### **Principles**

1. **Small** — one skill, one concept.
2. **Clean** — domain code does not know frameworks.
3. **Composable** — small pieces should combine over time.
4. **Sustainable** — no mega-prompts; keep human checkpoints.

---

## **Roadmap**

- **Phase 1** — Lightweight portable methodology pack using symlinks
- **Phase 2** — Claude Code / Codex / Cursor plugin marketplace packaging
- **Phase 3** — Standalone CLI built on Claude Agent SDK

---

## **Inspiration**

- [obra/superpowers](https://github.com/obra/superpowers) — multi-harness plugin structure
- [SuperClaude Framework](https://github.com/SuperClaude-Org/SuperClaude_Framework) — full-platform approach
- Eric Evans, *Domain-Driven Design*
- Vaughn Vernon, *Implementing Domain-Driven Design*
- Robert C. Martin, *Clean Architecture*

---

## **License**

MIT
