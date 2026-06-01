# OOPforge

![CI](https://github.com/LooSung/oopforge/actions/workflows/lint.yml/badge.svg)
![License](https://img.shields.io/github/license/LooSung/oopforge)

> **Forge small. Compose forever.**
>
> *A portable OOP/DDD methodology pack for AI coding agents.*

OOPforge helps AI coding agents design software around **domain models**, **aggregates**, **ports**, **adapters**, and **testable use cases** before implementation.

OOPforge gives Claude Code, Codex CLI, Cursor, and compatible coding agents a clear way to model software with **DDD**, **hexagonal architecture**, and **clean domain boundaries**.

[English](./README.md) · [한국어](./README.ko.md) · [日本語](./README.ja.md) · [中文](./README.zh.md)

---

## **Quickstart**

Install OOPforge into the agents detected on your machine:

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/LooSung/oopforge/main/scripts/setup/bootstrap.sh)"
```

Already installed? See [Setup commands](#setup-commands) below.

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

For Cursor Agent CLI:

```bash
cursor-agent --plugin-dir ~/.oopforge
```

```text
OOPforge Discovery: order domain. Start at Discovery — no code yet.
```

---

## **How to use OOPforge**

**New to the workflow?** Follow the step-by-step library loan guide:

**[Library loan walkthrough →](docs/guides/library-loan/README.md)**  
Discovery → Design → Skeleton → Implement (Java + Python) → Test

Guide index: [EN](docs/guides/library-loan/README.md) · [KO](docs/guides/library-loan/README.ko.md) · [JA](docs/guides/library-loan/README.ja.md) · [ZH](docs/guides/library-loan/README.zh.md)

| Resource | Purpose |
|---|---|
| [Library loan guide](docs/guides/library-loan/README.md) | Full tutorial — how to use OOPforge end to end |
| [examples/order-java](examples/order-java/) · [order-python](examples/order-python/) | Minimal runnable proof (place-order) |
| [Sample discovery (library)](docs/sample-output/discovery-library.md) | Short expected agent output ([KO](docs/sample-output/discovery-library.ko.md) · [JA](docs/sample-output/discovery-library.ja.md) · [ZH](docs/sample-output/discovery-library.zh.md)) |
| [Sample design (library)](docs/sample-output/design-library.md) | Short expected agent output ([KO](docs/sample-output/design-library.ko.md) · [JA](docs/sample-output/design-library.ja.md) · [ZH](docs/sample-output/design-library.zh.md)) |
| [Reviewer checklist](docs/reviewer-checklist.md) | Post-implement rule check |

Each workflow stage ends with a **human checkpoint** — do not skip ahead.

---

## **Why OOPforge**

OOPforge is a **DDD / OOP specialized AI engineering pack** — not a general agent framework.

| Principle | What it means |
|---|---|
| **Small** | One skill, one concept; 200 lines per skill |
| **Measurable** | 300 lines/file, 20 lines/method — reviewable units |
| **Workflow-first** | Discovery → Test with human checkpoints |
| **Proof over philosophy** | Runnable Java/Python examples, not slides |
| **Domain-first** | Framework import 0 in the domain layer |

In short: **structure is the default**, so agents stop generating God Services.

---

## **Before / After**

Most teams already know *what* DDD looks like in a diagram. The hard part is stopping the agent (or the team) from collapsing everything into a service class. OOPforge exists to make the **structure** the default.

### Before (typical Spring service)

```java
@Service
public class OrderService {
    public void createOrder(CreateOrderRequest req) {
        // validation, pricing, persistence, events — all in one class
        orderRepository.save(toEntity(req));
        eventPublisher.publish(...);
    }
}
```

**Problems:** God Service · no domain model · business rules scattered · hard to unit test · AI agents copy the same pattern

### After (OOPforge)

```java
Order order = Order.place(orderId, customerId, lines);   // domain
placeOrder.handle(command);                            // use case
orderRepository.save(order);                             // port
order.popEvents();                                       // OrderPlaced
```

```text
order/domain/Order.java              ← Aggregate Root (framework import 0)
order/application/provided/PlaceOrder.java
order/application/required/OrderRepository.java
order/application/service/PlaceOrderService.java
order/adapter/web/OrderController.java
order/adapter/persistence/InMemoryOrderRepository.java
```

**Effects:** domain-first · clear boundaries · domain tests without Spring · easier maintenance · agents follow a repeatable layout

Runnable reference: [`examples/order-java/`](./examples/order-java/) (Java) · [`examples/order-python/`](./examples/order-python/) (Python) — same place-order flow.

---

## **Installation**

### Setup commands

Run from `~/.oopforge` or this repo root:

```bash
./scripts/setup/install.sh          # install symlinks
./scripts/setup/doctor.sh           # check pack + links
./scripts/setup/install.sh update   # refresh symlinks after git pull
```

### **Automatic**

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/LooSung/oopforge/main/scripts/setup/bootstrap.sh)"
```

### **Manual**

```bash
git clone https://github.com/LooSung/oopforge ~/.oopforge
cd ~/.oopforge
chmod +x scripts/setup/*.sh
./scripts/setup/install.sh
./scripts/setup/doctor.sh
```

### **What gets installed**

`scripts/setup/install.sh` symlinks OOPforge into supported agent config directories:

| Agent | Status | Install target |
|---|---|---|
| **Claude Code** | Supported | `~/.claude/{skills,agents,commands}/oopforge` |
| **Codex CLI** | Supported | `~/.codex/skills/oopforge` |
| **Cursor Agent CLI** | Experimental | `cursor-agent --plugin-dir ~/.oopforge` |
| **OpenCode** | Experimental | `INSTALL_OPENCODE=1 ./scripts/setup/install.sh` |

Because the install uses symlinks, a `git pull` in `~/.oopforge` updates skill content immediately for linked agents.

To refresh install paths (for example after a version adds new link targets), run:

```bash
cd ~/.oopforge && git pull && ./scripts/setup/install.sh update
```

`./scripts/setup/install.sh update` runs `scripts/setup/uninstall.sh` then reinstalls all OOPforge symlinks. Use `./scripts/setup/install.sh --force` to replace existing symlinks without a full uninstall.

**Cursor Agent CLI:** `cursor-agent --plugin-dir ~/.oopforge`. See [docs/cursor.md](./docs/cursor.md). Marketplace packaging is Phase 2 (no ETA).

**Claude Code:** [docs/claude-code.md](./docs/claude-code.md) · **OpenCode (experimental):** [docs/opencode.md](./docs/opencode.md)

---

## **Troubleshooting**

### Check installation

```bash
./scripts/setup/doctor.sh
```

### Reinstall (refresh symlinks)

```bash
./scripts/setup/uninstall.sh
./scripts/setup/install.sh
```

Or after `git pull`:

```bash
cd ~/.oopforge && git pull && ./scripts/setup/install.sh update
```

### Dry run (see planned actions)

```bash
./scripts/setup/install.sh --dry-run
INSTALL_CLAUDE=1 ./scripts/setup/install.sh --dry-run
```

### Force replace existing symlinks

```bash
./scripts/setup/install.sh --force
```

### Remove installation

```bash
./scripts/setup/uninstall.sh
```

### Run smoke test locally

```bash
./scripts/ci/smoke-test.sh
```

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
├── examples/
│   ├── order-java/      Runnable Java Spring hexagonal reference (Order)
│   └── order-python/    Runnable Python FastAPI hexagonal reference (Order)
├── docs/
│   ├── guides/library-loan/   Step-by-step walkthrough (start here)
│   ├── sample-output/         Short expected agent outputs
│   ├── cursor.md        Cursor setup guide
│   ├── claude-code.md   Claude Code setup guide
│   └── opencode.md      OpenCode opt-in guide
├── skills/
│   ├── workflow/        Discovery → Design → Delivery Plan → Skeleton
│   │                    → Implement → Test, plus Refactor
│   ├── oop/             Aggregate Root, Value Object, Repository Port,
│   │                    Domain Event, Bounded Context, Factory Method,
│   │                    Specification Pattern
│   └── lang/
│       ├── java/        Spring hexagonal layout, JPA repository
│       └── python/      Pydantic value objects, clean FastAPI layout
├── agents/              ddd-architect, domain-reviewer subagents
├── commands/            Claude Code slash commands for workflow stages
├── AGENTS.md            cross-agent repository instructions
├── CLAUDE.md            Claude Code bootstrap instructions
├── scripts/
│   ├── setup/           bootstrap, install, uninstall, doctor
│   │   └── lib/common.sh
│   ├── ci/              lint-skills.sh, smoke-test.sh
│   └── path-convention.md
└── .github/workflows/lint.yml  CI validation
```

### **Agent instruction files**

- **`AGENTS.md`** is the shared source of truth for Codex, Cursor, OpenCode, and other compatible agents.
- **`CLAUDE.md`** is a thin Claude Code entry point that imports `AGENTS.md`.

---

## **Hard Rules**

These are intentionally measurable:

- Domain layer framework imports: **0**
- One file: **300 lines or less** — fits a reviewable PR diff; beyond this, review quality drops
- One method: **20 lines preferred** — one responsibility, testable and nameable without scrolling
- One skill file: **200 lines or less** — one concept per agent context load; split when teaching two ideas
- Public methods use **use-case verbs**, not CRUD names
- No public setters; use **factory methods** and intention-revealing behavior
- Collections crossing boundaries are defensively copied or immutable
- Other aggregates are referenced by **ID only**
- No domain logic without tests
- Comments explain *why*; names explain *what*

---

## **Language Policy**

| Area | Language |
|---|---|
| README | English (primary), plus KO / JA / ZH translations |
| `AGENTS.md`, shell scripts, CI | English |
| Skill files (`skills/`) | Korean (default); English translations welcome via PR |

Scripts and agent instructions use English so contributors and CI share one vocabulary. Skill content stays Korean-first because the pack was written for Korean-speaking teams. A future `skills/en/` tree is possible if demand grows.

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
- **Phase 2** — Claude Code / Codex / Cursor plugin marketplace packaging (Cursor CLI works via `--plugin-dir` today; bootstrap symlink + marketplace pending)
- **Phase 3** — Standalone CLI built on Claude Agent SDK

---

## **Inspiration**

- Eric Evans, *Domain-Driven Design*
- Vaughn Vernon, *Implementing Domain-Driven Design*
- Robert C. Martin, *Clean Architecture*
- Kent Beck, *Test-Driven Development: By Example*

---

## **Reference**

Reference only — OOPforge is an independent project; links here are for packaging and layout ideas, not dependencies or endorsements.

- Multi-harness plugin structure: [obra/superpowers](https://github.com/obra/superpowers)

---

## **License**

MIT

---

## Review and sample outputs

- [Library loan walkthrough](docs/guides/library-loan/README.md) — **recommended starting point**
- [Reviewer checklist](docs/reviewer-checklist.md)
- [Sample discovery — library](docs/sample-output/discovery-library.md)
- [Sample design — library](docs/sample-output/design-library.md)
- [Sample discovery — order](docs/sample-output/discovery-order.md)
- [Sample design — order](docs/sample-output/design-order.md)
