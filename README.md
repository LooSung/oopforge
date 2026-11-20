# OOPforge

![CI](https://github.com/LooSung/oopforge/actions/workflows/lint.yml/badge.svg)
![Examples](https://github.com/LooSung/oopforge/actions/workflows/examples.yml/badge.svg)
![License](https://img.shields.io/github/license/LooSung/oopforge)

> **AI ships the feature. OOPforge keeps the architecture.**

OOPforge is a skill pack for coding agents working on **Java Spring** or
**Python FastAPI** backends, with experimental support for Kotlin Spring and for
TypeScript server code in a Next.js app. Before your agent writes business logic, it names
the domain model, the use-case boundary, and the ports. Then it checks the result
against measurable Hard Rules, which forbid God Services and framework code in
the domain.

Works with **Claude Code**, **Codex CLI**, and **Cursor Agent CLI**.

[English](./README.md) · [한국어](./README.ko.md)

## The Forge family

| Pack | For | Stack |
|---|---|---|
| [Compforge](https://github.com/LooSung/compforge) | Frontend | TypeScript + React |
| **OOPforge** (this repo) | Backend | Java Spring · Python FastAPI · Kotlin Spring and TypeScript Next.js (experimental) |
| [FuseForge](https://github.com/LooSung/fuseforge) | One feature across both | Coordinates Compforge + OOPforge (experimental) |

Each pack works on its own. In Claude Code, the `forge` marketplace offers all three.

## Install

**Claude Code**, from the plugin marketplace (experimental):

```text
/plugin marketplace add LooSung/oopforge
/plugin install oopforge@forge
```

If `forge` is already added from another Forge repo, skip the first line.
Plugin files sit outside your project, so allow reading them once:
[read permission](docs/setup/claude-code.md#plugin-marketplace-experimental).

**Codex CLI**, or Claude Code without plugins, with the install script:

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/LooSung/oopforge/main/scripts/setup/bootstrap.sh)"
```

The script clones `~/.oopforge` and links it into Claude Code and Codex. Pick one
path per harness, then restart your agent. Cursor needs one manual step: [Cursor setup](docs/setup/cursor.md).
Pinned releases, updates, and removal: [install guide](docs/setup/install.md).

## Use

Start your agent from **your backend project**, not from `~/.oopforge`:

```text
/oopforge:craft Add a single Email value object
/oopforge:refactor Move the loan rules out of the controller without changing behavior
/oopforge:review Review PR 42
```

| Harness | How to call |
|---|---|
| Claude Code | `/oopforge:craft <request>` |
| Codex CLI | `/skills` → **oopforge**, then `Use OOPforge craft: <request>` (no leading `/`) |
| Cursor Agent CLI | `cursor-agent --plugin-dir ~/.oopforge`, then `Use OOPforge craft: <request>` |

## Commands

| Command | Use it for | It never |
|---|---|---|
| `craft` | **Default.** A use case, a value object, a domain bug | Skips required stages or widens scope silently |
| `refactor` | Restructure without changing behavior | Adds features |
| `consult` | Ask, compare, review, or write one plan document | Changes implementation or test code |
| `test` | Run, write, or strengthen tests | Changes production behavior; E2E and infrastructure need approval |
| `crucible` | Plan → build → refactor → test one change in one request | Builds before you approve the plan |
| `review` | P1/P2/P3 findings on one diff, branch, or PR | Changes code or posts to a PR unless asked |
| `jira` | One Jira card, or the child tasks of one epic or story | Touches anything but those issues |

Not sure which one? Use `craft`. It picks the smallest path.

## How it works

1. **Contract first.** Before business logic, Craft states its Assumptions and
   an OOP Contract: aggregates, invariants, use cases, and ports.
2. **Smallest path.** Adding one value object stays small. A new domain or large
   feature goes through the full flow, and you approve each stage:

   ```text
   Discovery → Design → Delivery Plan → Skeleton → Implement → Test
   ```

3. **Checked.** Craft verifies the [Hard Rules](AGENTS.md#hard-rules) before it
   reports done: 300 lines per file, 20 per method, zero framework imports in
   the domain, one Aggregate per transaction.

Stacks: `java-spring-layered`, `java-spring-hexagonal`, `python-fastapi-layered`,
and `python-fastapi-clean`; experimental `kotlin-spring-layered`,
`kotlin-spring-hexagonal`, `typescript-next-layered`, and
`typescript-next-hexagonal`. Skeletons include OpenAPI/Swagger UI. Domain Events
and the outbox are core; Production Readiness is opt-in for deployment requests.

### Before → after

```java
// Before: God Service, no domain model, rules scattered, hard to test
@Service
public class CalculatorService {
    public CalculationResponse calculate(CalculateRequest req) {
        repository.save(toEntity(req));
        eventPublisher.publish(...);
    }
}

// After: the domain owns the rule; the use case only orchestrates
Calculation calc = Calculation.perform(id, operandA, operator, operandB);
calculationRepository.save(calc);
calc.popEvents();
```

## Project switches

One line each in your project's `AGENTS.md`:

| Line | Effect |
|---|---|
| `OOPforge continuity: off` | Stop keeping `.craft/` work notes. By default, execution tasks keep them and resume unfinished work before editing. |
| `OOPforge work dir: <path>` | Keep work notes somewhere other than `.craft/` |
| `OOPforge live run: on` | Let Craft and Refactor launch the app to check it |
| `OOPforge cleanup pass: on` | Let Refactor run `/simplify` after verification |

For non-blocking PR feedback in your backend, copy
[`templates/github/oopforge-domain-review.yml`](templates/github/oopforge-domain-review.yml).
Blocking gates are opt-in; see the
[reviewer checklist](docs/reference/reviewer-checklist.md#enforcement-policy).

## Learn more

- [Library loan walkthrough](docs/guides/library-loan/README.md): Discovery → Test, step by step
- [Examples](examples/README.md): twelve runnable calculators (Java, Python, and experimental Kotlin and TypeScript Next.js × layered, hexagonal, hexagonal-CQRS)
- Setup: [Claude Code](docs/setup/claude-code.md) · [Codex](docs/setup/codex.md) ·
  [Cursor](docs/setup/cursor.md) · [Install, update, remove](docs/setup/install.md)
- [Support scope](docs/reference/support-scope.md) ·
  [Proof runs](docs/proof/README.md), neutral ones included; no general
  effectiveness claim · [All docs](docs/README.md)
- [Changelog](CHANGELOG.md) · [Contributing](.github/CONTRIBUTING.md) ·
  [Agent notes for maintainers](AGENTS.md)

## License

MIT
