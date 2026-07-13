# OOPforge

![CI](https://github.com/LooSung/oopforge/actions/workflows/lint.yml/badge.svg)
![Examples](https://github.com/LooSung/oopforge/actions/workflows/examples.yml/badge.svg)
![License](https://img.shields.io/github/license/LooSung/oopforge)

> **AI ships the feature. OOPforge keeps the architecture.**
>
> *Harness engineering that stops vibe coding from wrecking your backend.*

**Forge small. Compose forever.** OOPforge defines OOP/DDD as a dialect your agent follows — skills are the grammar, hard rules are the lint, runnable `examples/` are the reference, and install + commands are the runtime. A methodology pack plus agent harness, not a general agent framework.

It gives Claude Code, Codex CLI, Cursor, and compatible agents a clear way to design around **domain models**, **aggregates**, **ports**, **adapters**, and **testable use cases** before writing code.

Specialized for **Java (Spring)** and **Python (FastAPI)** — pick **3-tier (Controller/Service/Repository)** or **hexagonal/clean**, with **OpenAPI/Swagger** built in.

[English](./README.md) · [한국어](./README.ko.md)

---

## **Quickstart**

### **1. Install**

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/LooSung/oopforge/main/scripts/setup/bootstrap.sh)"
```

Check the install:

```bash
~/.oopforge/scripts/setup/doctor.sh
```

### **2. Open your target project (not the pack)**

OOPforge lives in `~/.oopforge`. Your app code lives in **your backend repo**. Always start the agent from that project:

```bash
cd /path/to/your-backend-project
```

### **3. Restart / load your agent**

Restart Claude Code or Codex CLI so it picks up the new skills and commands.

**Cursor** has no install symlink — pass the pack on every launch:

```bash
cursor-agent --plugin-dir ~/.oopforge
```

### **4. Run Craft**

Entry point is **Craft** on every harness; only **how you invoke it** differs:

| Harness | Invoke |
|---|---|
| **Claude Code** | `/oopforge:craft <request>` — registered slash command |
| **Codex CLI** | `/skills` → pick **oopforge**, then prompt **without** a leading `/` (Codex reserves `/` for its own commands) |
| **Cursor Agent CLI** | After `--plugin-dir`, slash command or natural language (see [Cursor setup](docs/cursor.md)) |

**Claude Code:**

```text
/oopforge:craft Add a single Email value object
```

**Codex CLI** (after `/skills` → oopforge):

```text
Use OOPforge craft: Add a single Email value object
```

**Cursor:**

```text
/oopforge:craft Add a single Email value object
```

### **5. Update (manual — Releases do not auto-install)**

Publishing a GitHub Release does **not** update your machine. Pull the pack, then refresh symlinks:

```bash
cd ~/.oopforge && git pull && ./scripts/setup/install.sh update
```

Then restart the agent (Cursor: relaunch with `--plugin-dir`). See [Installation](#installation) for troubleshooting.

---

## **Advanced Usage**

For advisory requests, Craft recommends the smallest path without implementing (same on every harness).

Advanced users may ask Craft to start at a specific workflow stage such as Discovery, Design, Delivery Plan, Skeleton, Implement, Test, or Refactor.

**Stack identifiers**:

| Stack | Architecture | When |
|---|---|---|
| `java-spring-layered` | 3-tier (Controller/Service/Repository) | Small services, MVP |
| `java-spring-hexagonal` | Hexagonal (domain/application/adapter) | Complex domain, many adapters |
| `python-fastapi-layered` | 3-tier (Router/Service/Repository) | Small services, MVP |
| `python-fastapi-clean` | Clean (domain/application/infrastructure/presentation) | Complex domain |

All backend skeletons ship with **OpenAPI/Swagger UI** enabled by default (springdoc / FastAPI built-in).

Already installed? See [Installation](#installation) for manual setup, updates, and troubleshooting.

**Remember:** a new [GitHub Release](https://github.com/LooSung/oopforge/releases) does not update `~/.oopforge` by itself — use Quickstart step 5.

Harness guides: [Claude Code](docs/claude-code.md) · [Codex](docs/codex.md) · [Cursor](docs/cursor.md)

---

## **How to use OOPforge**

**New to the workflow?** Follow the step-by-step library loan guide:

**[Library loan walkthrough →](docs/guides/library-loan/README.md)**  
Discovery → Design → Skeleton → Implement (Java + Python) → Test

Guide index: [EN](docs/guides/library-loan/README.md) · [KO](docs/guides/library-loan/README.ko.md)

| Resource | Purpose |
|---|---|
| [Library loan guide](docs/guides/library-loan/README.md) | Full tutorial — how to use OOPforge end to end |
| [Examples index](examples/README.md) | Runnable proof — same calculator, 6 examples |
| [calculator-java-layered](examples/calculator-java-layered/) · [calculator-java-hexagonal](examples/calculator-java-hexagonal/) · [calculator-java-hexagonal-cqrs](examples/calculator-java-hexagonal-cqrs/) | Java 3-tier · hexagonal · hexagonal + CQRS |
| [calculator-python-layered](examples/calculator-python-layered/) · [calculator-python-hexagonal](examples/calculator-python-hexagonal/) · [calculator-python-hexagonal-cqrs](examples/calculator-python-hexagonal-cqrs/) | FastAPI 3-tier · hexagonal · hexagonal + CQRS |
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
public class CalculatorService {
    public CalculationResponse calculate(CalculateRequest req) {
        // parsing, computing, persistence, history, formatting — all in one class
        repository.save(toEntity(req));
        eventPublisher.publish(...);
    }
}
```

**Problems:** God Service · no domain model · business rules scattered · hard to unit test · AI agents copy the same pattern

### After (OOPforge)

```java
Calculation calc = Calculation.perform(id, operandA, operator, operandB);  // domain
calculate.handle(command);                                  // use case
calculationRepository.save(calc);                           // port
calc.popEvents();                                           // CalculationPerformed
```

```text
calculator/domain/Calculation.java   ← Aggregate Root (framework import 0)
calculator/application/provided/Calculate.java
calculator/application/required/CalculationRepository.java
calculator/application/service/CalculateService.java
calculator/adapter/web/CalculatorController.java
calculator/adapter/persistence/InMemoryCalculationRepository.java
```

**Effects:** domain-first · clear boundaries · domain tests without Spring · easier maintenance · agents follow a repeatable layout

Runnable reference: [examples/README.md](examples/README.md) — the same calculator across layered, hexagonal, and CQRS stacks.

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

`install.sh` links `skills/SKILL.md` as the Codex skill entry point. Codex reserves `/` for built-ins — do **not** type `/oopforge:craft`. After `/skills` → **oopforge**:

```text
Use OOPforge craft: <request>
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

### **Memory store (resume across sessions)**

OOPforge keeps a lightweight memory so work survives between chats. Write it down, and pull it back when you need it.

- Each work item **may** get one document at `.craft/<kind>-<slug>.md` (for example `.craft/feature-member-management.md`), tracking decisions, progress, and the next step. Craft **asks first**; skip if you do not need session memory.
- When you return, Craft reads the matching document **first** and continues from there.
- `.craft/` is gitignored by default (personal notes). Override the location with an `OOPforge work dir: <path>` line in your project `AGENTS.md`.

See [`skills/workflow/continuity.md`](skills/workflow/continuity.md).

---

## **What's Inside**

```text
oopforge/
├── examples/
│   ├── README.md        Stack ↔ folder index
│   ├── calculator-java-layered/      Java Spring 3-tier
│   ├── calculator-java-hexagonal/    Java Spring hexagonal
│   ├── calculator-java-hexagonal-cqrs/  Java Spring hexagonal + CQRS
│   ├── calculator-python-layered/    FastAPI 3-tier
│   ├── calculator-python-hexagonal/  FastAPI hexagonal/clean
│   └── calculator-python-hexagonal-cqrs/  FastAPI hexagonal + CQRS
├── docs/
│   ├── roadmap.md             Direction, priorities, non-goals
│   ├── guides/library-loan/   Step-by-step walkthrough (start here)
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
│   ├── lang/            Backend stack selection (layered vs hexagonal/clean)
│   └── skeleton/        Backend package structure + empty types
├── commands/            Claude Code slash command entry point
│                        + /oopforge:craft
├── AGENTS.md            cross-agent repository instructions
├── CLAUDE.md            Claude Code bootstrap instructions
├── scripts/
│   ├── setup/           bootstrap, install, uninstall, doctor
│   │   └── lib/common.sh
│   ├── ci/              lint-skills.sh, smoke-test.sh
│   └── path-convention.md
└── .github/workflows/   lint.yml, examples.yml (CI)
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
| README & docs | English (primary) + Korean only; other languages only on request |
| `AGENTS.md`, shell scripts, CI | English |
| Skill files (`skills/`) | **English (canonical)** — these are agent-facing instructions |

Skills, scripts, and agent instructions are English so the agent reads its native instruction language and contributors/CI share one vocabulary. Korean speakers read the methodology in one place: **[docs/methodology.ko.md](./docs/methodology.ko.md)** — a conceptual guide, not a per-skill mirror (mirrors drift; a concept guide stays stable).

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
- Skill routing and "smallest path" philosophy: [pstack by Lauren (Cursor)](https://cursor.com/en-US/lp-team/lauren)

---

## **License**

MIT

---

## Review and sample outputs

- [Library loan walkthrough](docs/guides/library-loan/README.md) — **recommended starting point**
- [Reviewer checklist](docs/reviewer-checklist.md)
