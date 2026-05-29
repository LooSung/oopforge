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
| **Cursor** | Not yet (Phase 2) | No installer — manifest only at `.cursor-plugin/` |
| **OpenCode** | Experimental | `INSTALL_OPENCODE=1 ./install.sh` |

Because the install uses symlinks, a `git pull` in `~/.oopforge` updates skill content immediately for linked agents.

To refresh install paths (for example after a version adds new link targets), run:

```bash
cd ~/.oopforge && git pull && ./install.sh update
```

`./install.sh update` runs `uninstall.sh` then reinstalls all OOPforge symlinks. Use `./install.sh --force` to replace existing symlinks without a full uninstall.

**Cursor today:** copy or reference `AGENTS.md` in your project. See [docs/cursor.md](./docs/cursor.md). Marketplace packaging is planned for Phase 2 with no ETA yet.

**Claude Code:** [docs/claude-code.md](./docs/claude-code.md) · **OpenCode (experimental):** [docs/opencode.md](./docs/opencode.md)

---

## **Troubleshooting**

### Check installation

```bash
./doctor.sh
```

### Reinstall (refresh symlinks)

```bash
./uninstall.sh
./install.sh
```

Or after `git pull`:

```bash
cd ~/.oopforge && git pull && ./install.sh update
```

### Dry run (see planned actions)

```bash
./install.sh --dry-run
INSTALL_CLAUDE=1 ./install.sh --dry-run
```

### Force replace existing symlinks

```bash
./install.sh --force
```

### Remove installation

```bash
./uninstall.sh
```

### Run smoke test locally

```bash
./scripts/smoke-test.sh
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
├── bootstrap.sh         one-line installer
├── doctor.sh            installation checker
├── install.sh           symlink installer
├── scripts/lint-skills.sh  skill frontmatter and repo lint
├── scripts/smoke-test.sh   install/doctor smoke test
├── uninstall.sh         symlink remover
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
- **Phase 2** — Claude Code / Codex / Cursor plugin marketplace packaging (Cursor: no ETA; manifest exists, installer pending)
- **Phase 3** — Standalone CLI built on Claude Agent SDK

---

## **Inspiration**

- Eric Evans, *Domain-Driven Design*
- Vaughn Vernon, *Implementing Domain-Driven Design*
- Robert C. Martin, *Clean Architecture*

---

## **License**

MIT
