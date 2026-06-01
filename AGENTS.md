# OOPforge — Agent Instructions

If you are an AI coding agent working in this repository, follow OOPforge itself.

## Mission

OOPforge is a portable OOP/DDD methodology pack for coding agents — **methodology plus agent harness**.

It defines OOP/DDD as a **dialect agents follow** (skills = grammar, hard rules = lint, `examples/` = reference implementations, install/commands = runtime). Protect the core promise: small skills, clean domain models, explicit workflow stages, and human checkpoints.

## Required Workflow

For new domains or large features, do not jump straight to code.

1. **Discovery** — read `skills/workflow/discovery.md`; produce glossary, contexts, actors, open questions.
2. **Design** — read `skills/workflow/design.md`; produce use-case signatures, aggregate outlines, ports.
3. **Delivery Plan** — read `skills/workflow/delivery-plan.md`; align requirements, scope, implementation order, tests, and release risks.
4. **Skeleton** — read `skills/workflow/skeleton.md`; create package structure and empty interfaces/classes only.
5. **Implement** — read `skills/workflow/implement.md`; implement one use case with tests.
6. **Test** — read `skills/workflow/test.md`; run unit, integration, and E2E checks as needed.

Ask for human approval before moving from one stage to the next.

**For smaller, focused tasks** (extending an existing domain, adding a single value object, refactoring, code review) — start with `/oopforge:route` (`commands/route.md`). It picks the minimal skill/command instead of forcing the full pipeline.

## Skill Path Convention

Resolve the OOPforge pack root in order: `$OOPFORGE_HOME` → `~/.oopforge` → repository root (when developing this pack).

Skill files live at `{pack}/skills/...`. Do **not** use legacy `skills/oopforge/...` paths. See `scripts/path-convention.md`.

## Skill Routing

Use this table to decide **which skill to read first**. Workflow stage always wins over ad-hoc coding.

| Workflow stage | Goal | Read first | Agent (optional) |
|---|---|---|---|
| Route (intent triage) | Pick the smallest skill/command for the user's actual goal | `commands/route.md` | — |
| Discovery | Glossary, contexts, actors | `skills/workflow/discovery.md` | `@ddd-architect` |
| Design | Use-case signatures, aggregates | `skills/workflow/design.md` + relevant `skills/oop/*` | `@ddd-architect` |
| Delivery Plan | Scope, order, tests, risks | `skills/workflow/delivery-plan.md` | — |
| Skeleton | Packages, empty types | `skills/workflow/skeleton.md` + lang layout skill | `@ddd-architect` |
| Implement | One use case + tests | `skills/workflow/implement.md` + oop/lang skills | `@ddd-architect` |
| Test | Unit / integration / E2E | `skills/workflow/test.md` | — |
| Refactor | Behavior-preserving cleanup | `skills/workflow/refactor.md` | `@domain-reviewer` |
| Code review | Detect rule violations | Hard Rules below + `examples/order-java/` | `@domain-reviewer` |

### Task → skill (within a stage)

| Task | Skill |
|---|---|
| Aggregate design | `skills/oop/aggregate-root.md` |
| Value object | `skills/oop/value-object.md` |
| Use case / application service | `skills/oop/application-service.md` |
| Repository port | `skills/oop/repository-port.md` |
| Domain event | `skills/oop/domain-event.md` |
| Bounded context | `skills/oop/bounded-context.md` |
| Java package layout — 3-tier | `skills/lang/java/spring-layered-layout.md` |
| Java package layout — hexagonal | `skills/lang/java/spring-hexagonal-layout.md` |
| JPA adapter | `skills/lang/java/jpa-repository.md` |
| Python layout — FastAPI 3-tier | `skills/lang/python/fastapi-layered-layout.md` |
| Python layout — FastAPI clean | `skills/lang/python/clean-fastapi-layout.md` |
| Python aggregate | `skills/lang/python/python-aggregate.md` |
| Python domain event | `skills/lang/python/python-domain-event.md` |
| Pydantic value object | `skills/lang/python/pydantic-value-object.md` |
| OpenAPI / Swagger conventions | `skills/lang/api/openapi-conventions.md` |

### Harness setup

| Harness | Guide |
|---|---|
| Codex | `docs/codex.md` |
| Claude Code | `docs/claude-code.md` |
| Cursor | `docs/cursor.md` |
| OpenCode (experimental) | `docs/opencode.md` |

Reference implementation: [examples/README.md](examples/README.md) — `order-java`, `order-java-layered`, `order-python`, `order-python-layered` (same place-order flow).

## Skill Selection

Before changing behavior, read the relevant skill file:

- Aggregate design: `skills/oop/aggregate-root.md`
- Value objects: `skills/oop/value-object.md`
- Application services: `skills/oop/application-service.md`
- Repository ports: `skills/oop/repository-port.md`
- Domain events: `skills/oop/domain-event.md`
- Bounded contexts: `skills/oop/bounded-context.md`
- Factory methods: `skills/oop/factory-method.md`
- Specification pattern: `skills/oop/specification-pattern.md`
- Java layouts: `skills/lang/java/spring-layered-layout.md` (3-tier) · `skills/lang/java/spring-hexagonal-layout.md` (hexagonal)
- JPA repositories: `skills/lang/java/jpa-repository.md`
- Python layouts: `skills/lang/python/fastapi-layered-layout.md` (FastAPI 3-tier) · `skills/lang/python/clean-fastapi-layout.md` (FastAPI clean)
- Python patterns: `skills/lang/python/python-aggregate.md` · `skills/lang/python/python-domain-event.md` · `skills/lang/python/pydantic-value-object.md`
- API contracts: `skills/lang/api/openapi-conventions.md`
- Delivery planning: `skills/workflow/delivery-plan.md`
- Testing: `skills/workflow/test.md`
- Refactoring existing or external code: `skills/workflow/refactor.md`
- Roadmap / direction: `docs/roadmap.md`

## Hard Rules

These limits are intentionally measurable. They come from review focus and agent context size, not arbitrary style:

- **300 lines/file** — a diff a reviewer can hold in working memory (~15-minute review unit)
- **20 lines/method** — one responsibility, testable and nameable without scrolling
- **200 lines/skill** — one concept per agent context load; split when a skill teaches two ideas

- Domain layer framework imports: **0**
- One file: **300 lines or less**
- One method: **20 lines preferred**
- One skill file: **200 lines or less**
- No public setters; use factory methods or intention-revealing behavior methods.
- Collections crossing boundaries must be defensively copied or immutable.
- Other aggregates are referenced by ID only.
- Do not commit domain logic without tests.
- Comments explain "why"; names explain "what".

## Repository Discipline

- Keep harness packaging portable: Claude and Codex install via `install.sh`; Cursor Agent CLI loads via `cursor-agent --plugin-dir` (experimental, not in `install.sh`); OpenCode is experimental/opt-in.
- Do not add runtime dependencies for installer scripts unless there is no simpler shell-based alternative.
- Update `CHANGELOG.md` for user-visible changes.
- When changing install behavior, verify with a clean temporary `HOME`.
- Do not claim a harness integration works until documented setup steps and a clean-session smoke test prove it. For Cursor, verify `cursor-agent --plugin-dir` loads skills before documenting.

## What Not To Do

- Do not merge workflow stages to save time.
- Do not add framework annotations or infrastructure concerns to domain examples.
- Do not create mega-prompts, mega-skills, or broad abstractions without evidence.
- Do not make OpenCode part of the default install path unless its integration becomes stable.
- Do not mix refactoring with feature changes; use `workflow-refactor` only for behavior-preserving cleanup.
