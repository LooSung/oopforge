# OOPforge

![CI](https://github.com/LooSung/oopforge/actions/workflows/lint.yml/badge.svg)
![License](https://img.shields.io/github/license/LooSung/oopforge)

> **Forge small. Compose forever.**
>
> *A portable OOP/DDD methodology pack for AI coding agents.*

**OOPforge defines OOP/DDD as a dialect agents follow**, and runs that dialect through skills, workflow, runnable examples, and install — **methodology pack plus agent harness** (not a general agent framework).

OOPforge helps AI coding agents design software around **domain models**, **aggregates**, **ports**, **adapters**, and **testable use cases** before implementation.

OOPforge gives Claude Code, Codex CLI, Cursor, and compatible coding agents a clear way to model software with **DDD**, **layered (3-tier) or hexagonal/clean architecture**, **OpenAPI-first contracts**, and **clean domain boundaries** — for Java (Spring) and Python (FastAPI).

[English](./README.md) · [한국어](./README.ko.md) · [日本語](./README.ja.md) · [中文](./README.zh.md)

---

## **Quickstart**

Install OOPforge into the agents detected on your machine:

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/LooSung/oopforge/main/scripts/setup/bootstrap.sh)"
```

Already installed? See [Setup commands](#setup-commands) below.

Then use Craft as the single entry point. It inspects the request, picks the smallest appropriate path, and only implements when the request calls for it:

```text
/oopforge:craft Add a single Email value object
/oopforge:craft Add a refund feature to the payment domain
/oopforge:craft Refactor OrderService without changing behavior
```

For advisory requests, `/oopforge:craft` recommends the smallest path without implementing.

Advanced users may ask Craft to start at a specific workflow stage such as Discovery, Design, Delivery Plan, Skeleton, Implement, Test, or Refactor.

**Stack identifiers**:

| Stack | Architecture | When |
|---|---|---|
| `java-spring-layered` | 3-tier (Controller/Service/Repository) | Small services, MVP |
| `java-spring-hexagonal` | Hexagonal (domain/application/adapter) | Complex domain, many adapters |
| `python-fastapi-layered` | 3-tier (Router/Service/Repository) | Small services, MVP |
| `python-fastapi-clean` | Clean (domain/application/infrastructure/presentation) | Complex domain |

All backend skeletons ship with **OpenAPI/Swagger UI** enabled by default (springdoc / FastAPI built-in).

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
| [Examples index](examples/README.md) | Runnable proof — 4 stacks, same place-order |
| [order-java](examples/order-java/) · [order-java-layered](examples/order-java-layered/) | Java hexagonal · Java 3-tier |
| [order-python](examples/order-python/) · [order-python-layered](examples/order-python-layered/) | FastAPI clean · FastAPI 3-tier |
| [Sample discovery (library)](docs/sample-output/discovery-library.md) | Short expected agent output ([KO](docs/sample-output/discovery-library.ko.md) · [JA](docs/sample-output/discovery-library.ja.md) · [ZH](docs/sample-output/discovery-library.zh.md)) |
| [Sample design (library)](docs/sample-output/design-library.md) | Short expected agent output ([KO](docs/sample-output/design-library.ko.md) · [JA](docs/sample-output/design-library.ja.md) · [ZH](docs/sample-output/design-library.zh.md)) |
| [Reviewer checklist](docs/reviewer-checklist.md) | Post-implement rule check |

Each workflow stage ends with a **human checkpoint** — do not skip ahead.

---

## **Why OOPforge**

OOPforge is a **DDD / OOP specialized AI engineering pack** — not a general agent framework. Think of it as **harness engineering for an OOP dialect**: skills encode grammar, hard rules act as lint, examples are reference implementations, and install/commands wire agents to the runtime.

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

Runnable reference: [examples/README.md](examples/README.md) — same place-order flow across hexagonal and layered stacks.

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
| **Claude Code** | Supported | `~/.claude/{skills,commands}/oopforge` |
| **Codex CLI** | Supported via skill entry point | `~/.codex/skills/oopforge` |
| **Cursor Agent CLI** | Experimental | `cursor-agent --plugin-dir ~/.oopforge` |

Because the install uses symlinks, a `git pull` in `~/.oopforge` updates skill content immediately for linked agents.

### **Claude Code**

`install.sh` links both skills and commands. Restart Claude Code, then use:

```text
/oopforge:craft <request>
```

### **Codex CLI**

`install.sh` links `skills/SKILL.md` as the Codex skill entry point. Type the Craft prompt as normal text:

```text
/oopforge:craft <request>
```

### **Cursor Agent CLI**

Cursor loads OOPforge with `--plugin-dir` instead of an install symlink:

```bash
cursor-agent --plugin-dir ~/.oopforge
```

Then ask naturally, or include the Craft prompt in your request.

To refresh install paths (for example after a version adds new link targets), run:

```bash
cd ~/.oopforge && git pull && ./scripts/setup/install.sh update
```

`./scripts/setup/install.sh update` runs `scripts/setup/uninstall.sh` then reinstalls all OOPforge symlinks. Use `./scripts/setup/install.sh --force` to replace existing symlinks without a full uninstall.

More setup details: [Claude Code](docs/claude-code.md) · [Codex](docs/codex.md) · [Cursor](docs/cursor.md)

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

**For smaller, focused tasks** (one value object, extending an existing domain, refactoring, code review) — start with `/oopforge:craft`. It picks the minimal path instead of forcing the full pipeline.

| Stage | Output | Do not do |
|---|---|---|
| **1. Discovery** | Glossary, bounded contexts, actors, open questions | Code |
| **2. Design** | Use-case signatures, aggregate outlines, ports | Implementation |
| **3. Delivery Plan** | Scope, contract, implementation order, test/release plan | Coding |
| **4. Skeleton** | Packages, interfaces, empty classes | Business logic |
| **5. Implement** | One use case at a time | Multiple use cases at once |
| **6. Test** | Unit, integration, E2E checks | Untested domain logic |

Each stage ends with a human checkpoint before moving on.

### **Where to start**

- **Start here** → `/oopforge:craft <what you want>` — recommends or performs the smallest suitable OOP path.
- Start at **Discovery** for a new domain or unclear feature.
- Start at **Delivery Plan** if Discovery/Design already exist.
- Start at **Implement** only when the contract and skeleton are already clear.
- Use **Test** whenever you need TDD, regression coverage, or E2E verification.
- Use **Refactor** separately when behavior must stay the same.

**Refactor is intentionally outside the default feature flow.** Use it for existing or imported code that needs cleanup without behavior changes.

Advanced users may invoke individual workflow stages through Craft, for example "Start at Discovery", "Create a delivery plan", or "Run the test workflow".

---

## **What's Inside**

```text
oopforge/
├── examples/
│   ├── README.md        Stack ↔ folder index
│   ├── order-java/      Java Spring hexagonal
│   ├── order-java-layered/  Java Spring 3-tier
│   ├── order-python/    Python FastAPI hexagonal
│   └── order-python-layered/  FastAPI 3-tier
├── docs/
│   ├── roadmap.md             Direction, priorities, non-goals
│   ├── guides/library-loan/   Step-by-step walkthrough (start here)
│   ├── sample-output/         Short expected agent outputs
│   ├── codex.md         Codex setup guide
│   ├── cursor.md        Cursor setup guide
│   └── claude-code.md   Claude Code setup guide
├── skills/
│   ├── SKILL.md         Codex skill entry point
│   ├── workflow/        Discovery → Design → Delivery Plan → Skeleton
│   │                    → Implement → Test, plus Refactor
│   ├── principles/      OOP decision principles
│   ├── playbooks/       Craft task checklists
│   ├── oop/             Domain model + use-case boundary
│   └── lang/            Backend layout for Java Spring and Python FastAPI
├── commands/            Claude Code slash command entry point
│                        + /oopforge:craft
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

- **`AGENTS.md`** is the shared source of truth for Codex, Cursor, and other compatible agents.
- **`CLAUDE.md`** is a thin Claude Code entry point that imports `AGENTS.md`.

---

## **Hard Rules**

The enforceable, measurable rules live in [`AGENTS.md`](./AGENTS.md). README keeps the user-facing overview; agents should use `AGENTS.md` as the source of truth for rule checks.

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

Packaging phases:

- **Phase 1** — Lightweight portable methodology pack using symlinks
- **Phase 2** — Claude Code / Codex / Cursor plugin marketplace packaging (Cursor CLI works via `--plugin-dir` today; bootstrap symlink + marketplace pending)
- **Phase 3** — Standalone CLI built on Claude Agent SDK

Direction, priorities, and non-goals (short/medium/long term, language expansion, lint enforcement, anti-pattern catalog): **[docs/roadmap.md](./docs/roadmap.md)**

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
