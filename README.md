# OOPforge

![CI](https://github.com/LooSung/oopforge/actions/workflows/lint.yml/badge.svg)
![Examples](https://github.com/LooSung/oopforge/actions/workflows/examples.yml/badge.svg)
![License](https://img.shields.io/github/license/LooSung/oopforge)

> **AI ships the feature. OOPforge keeps the architecture.**
>
> *Harness engineering that stops vibe coding from wrecking your backend.*

**Forge small. Compose forever.** OOPforge is a portable OOP/DDD methodology
pack and agent harness. Skills teach the grammar, hard rules act as lint,
runnable examples provide references, and Craft selects the smallest workflow
for the job.

Use it when a **Java (Spring)** or **Python (FastAPI)** backend needs explicit
domain models, use-case boundaries, and reviewable architecture. It is not a
general agent framework, UI toolkit, or automatic code generator.

[Positioning and non-goals](docs/positioning.md) ·
[Reproducible proof protocol](docs/proof/README.md)

[English](./README.md) · [한국어](./README.ko.md)

## Quickstart

### 1. Install the latest `main`

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/LooSung/oopforge/main/scripts/setup/bootstrap.sh)"
```

The bootstrap clones or updates `~/.oopforge` and installs detected Claude Code
and Codex links. It does not configure Cursor automatically.

### 2. Check the pack and installed links

```bash
~/.oopforge/scripts/setup/doctor.sh
```

`doctor.sh` validates the pack and available symlinks. A successful result does
not prove that a running agent loaded Craft; use the harness-specific check in
step 4. If it warns that your chosen Claude or Codex link is missing, run
`INSTALL_CLAUDE=1 ~/.oopforge/scripts/setup/install.sh` or the Codex equivalent.

### 3. Open your backend project

OOPforge lives in `~/.oopforge`. Your app code lives in **your backend repo**. Always start the agent from that project:

```bash
cd /path/to/your-backend-project
```

### 4. Load Craft and make one request

Choose the harness you actually use:

| Harness | Load and invoke Craft |
|---|---|
| **Claude Code** | Restart Claude Code, then `/oopforge:craft <request>` |
| **Codex CLI** | Restart Codex, use `/skills` to select **oopforge**, then prompt without a leading `/` |
| **Cursor Agent CLI** | Register and explicitly load the local plugin, then use `Use OOPforge craft: …` |

Claude Code:

```text
/oopforge:craft Add a single Email value object
```

Codex CLI:

```text
Use OOPforge craft: Add a single Email value object
```

Cursor Agent CLI requires one extra registration step:

```bash
mkdir -p ~/.cursor/plugins/local
ln -s ~/.oopforge ~/.cursor/plugins/local/oopforge
cd /path/to/your-backend-project
cursor-agent --plugin-dir ~/.cursor/plugins/local/oopforge
```

```text
Use OOPforge craft: Add a single Email value object
```

For a fresh execution task, a loaded Craft flow identifies the smallest path
and surfaces Assumptions and an OOP Contract before business logic. Advisory
requests recommend a path without implementing. See the
[illustrative Craft session](docs/assets/craft-demo.cast) and the exact setup
guides for [Claude Code](docs/claude-code.md), [Codex](docs/codex.md), and
[Cursor](docs/cursor.md).

## The Basic Workflow

Craft is the single entry point. It selects a focused path for small changes and
preserves the full sequence for a new domain or large feature:

```text
Discovery → Design → Delivery Plan → Skeleton → Implement → Test
```

| Stage | Output | Do not do |
|---|---|---|
| **Discovery** | Glossary, contexts, actors, open questions | Code |
| **Design** | Use-case signatures, aggregate outlines, ports | Implementation |
| **Delivery Plan** | Scope, order, tests, release risks | Coding |
| **Skeleton** | Packages, interfaces, empty classes | Business logic |
| **Implement** | One tested use case at a time | Multiple use cases at once |
| **Test** | Unit, integration, and E2E evidence | Untested domain logic |

Each stage ends with a human checkpoint. Ask Craft to start at a named stage
only when earlier decisions already exist. Refactoring stays outside the feature
flow because it must preserve behavior.

Supported stack identifiers are `java-spring-layered`,
`java-spring-hexagonal`, `python-fastapi-layered`, and
`python-fastapi-clean`. Backend skeletons include OpenAPI/Swagger UI.

### Resume work across sessions

Execution tasks keep lightweight notes under `.craft/`. If unfinished work
exists, Craft presents a Resume block before editing. When a session ends with
work remaining, `.craft/next-session-prompt.md` records the next decision.

## Learn by example

**New to the workflow?** Follow the step-by-step library loan guide:

**[Library loan walkthrough →](docs/guides/library-loan/README.md)**  
Discovery → Design → Skeleton → Implement (Java + Python) → Test

Guide index: [EN](docs/guides/library-loan/README.md) · [KO](docs/guides/library-loan/README.ko.md)

| Resource | Purpose |
|---|---|
| [Library loan guide](docs/guides/library-loan/README.md) | End-to-end tutorial |
| [Examples index](examples/README.md) | Six runnable calculator references |
| [Reviewer checklist](docs/reviewer-checklist.md) | Post-implementation rule check |

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

## Before / After

Most teams know the DDD diagram. The hard part is stopping an agent from
collapsing the implementation into one service class.

### Before

```java
@Service
public class CalculatorService {
    public CalculationResponse calculate(CalculateRequest req) {
        repository.save(toEntity(req));
        eventPublisher.publish(...);
    }
}
```

**Problems:** God Service · no domain model · scattered rules · hard-to-test code

### After

```java
Calculation calc = Calculation.perform(id, operandA, operator, operandB);
calculate.handle(command);
calculationRepository.save(calc);
calc.popEvents();
```

**Effects:** domain-first · clear boundaries · framework-free domain tests · a
repeatable layout. See the runnable [examples](examples/README.md).

### Evidence and limits

The [proof protocol](docs/proof/README.md) fixes the task, control, treatment,
evaluation rules, and publication standard. Three valid Cursor
`gpt-5.6-sol-high` pairs are published:
[pair 1](docs/proof/results/2026-08-20-cursor-gpt-5.6-sol-high.md) was
neutral; [pair 2](docs/proof/results/2026-08-20-cursor-gpt-5.6-sol-high-2.md)
and [pair 3](docs/proof/results/2026-08-20-cursor-gpt-5.6-sol-high-3.md) were
favorable on method length. All three leaked public mutable invariant state.
See the [repeated-pair summary](docs/proof/README.md#repeated-pair-summary).
This is not a general effectiveness claim.

## Installation, updates, and removal

The Quickstart bootstrap tracks the latest `main`. To install a reproducible
release instead:

```bash
git clone https://github.com/LooSung/oopforge ~/.oopforge
cd ~/.oopforge
git checkout v0.13.0
chmod +x scripts/setup/*.sh
./scripts/setup/install.sh
./scripts/setup/doctor.sh
```

### Install targets

| Harness | Installed or registered path |
|---|---|
| **Claude Code** | `~/.claude/skills/oopforge` and `~/.claude/commands/oopforge` |
| **Codex CLI** | `~/.codex/skills/oopforge` |
| **Cursor Agent CLI** | Manual local plugin or project-local skill; `install.sh` does not configure it |

`install.sh` only creates Claude and Codex links when their config directories
exist. Set `INSTALL_CLAUDE=1` or `INSTALL_CODEX=1` to create a missing target
explicitly.

### Update

A GitHub Release does not update an existing clone. Pull the pack, refresh
Claude/Codex link targets, and restart the agent:

```bash
cd ~/.oopforge && git pull && ./scripts/setup/install.sh update
```

That command is for a `main`-tracking clone. A release-pinned clone must
`git fetch --tags`, check out the chosen newer tag, and then run
`./scripts/setup/install.sh update`.

Cursor's manually registered symlink is not managed by `install.sh`; after the
pull, restart `cursor-agent`.

### Verify and troubleshoot

Run these commands from `~/.oopforge`:

```bash
./scripts/setup/doctor.sh              # pack structure and installed links
./scripts/setup/install.sh --dry-run   # planned link changes
./scripts/setup/install.sh --force     # replace conflicting symlinks
./scripts/ci/smoke-test.sh             # isolated Claude/Codex install lifecycle
```

These checks do not execute a live Craft response. Verify activation with the
entry point documented in the relevant harness guide:
[Claude Code](docs/claude-code.md) · [Codex](docs/codex.md) ·
[Cursor](docs/cursor.md).

### Remove

```bash
./scripts/setup/uninstall.sh
```

This removes only OOPforge-managed Claude and Codex links. It deliberately
keeps `~/.oopforge`, Cursor's `~/.cursor/plugins/local/oopforge` link, and any
project-local `.cursor/skills/oopforge` link. Remove those paths manually if
you want a complete uninstall.

## What's included

- `skills/` — workflow, OOP/DDD, stack, skeleton, and review instructions
- `commands/` — Claude Code command entry point
- `examples/` — six runnable Java/Python calculator references
- `docs/` — harness guides, proof protocol, roadmap, and walkthroughs
- `scripts/` — setup, lint, architecture checks, and smoke tests
- `templates/github/` — reusable target-project domain review

Agents use [`AGENTS.md`](./AGENTS.md) as the shared rule source;
[`CLAUDE.md`](./CLAUDE.md) is the Claude Code adapter. Target backends can use
[`templates/github/oopforge-domain-review.yml`](templates/github/oopforge-domain-review.yml) for
non-blocking PR feedback. Blocking gates are opt-in; see the [reviewer checklist](docs/reviewer-checklist.md#enforcement-policy).

## Project policy

The enforceable rules live in [`AGENTS.md`](./AGENTS.md). Skill files, scripts,
CI, and agent instructions use English as their canonical language. Korean
readers can use the conceptual
[`docs/methodology.ko.md`](./docs/methodology.ko.md) guide instead of unstable
per-skill translations.

OOPforge remains a backend OOP/DDD methodology layer, not a model wrapper or
general orchestration framework. See the [roadmap](./docs/roadmap.md) for
required future work and non-goals, and the
[changelog](./CHANGELOG.md) for completed releases.

## License

MIT
