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

**For smaller, focused tasks** (extending an existing domain, adding a single value object, refactoring, code review) — start with `/oopforge:craft` (`commands/craft.md`). It selects the smallest path and does not force the full pipeline.

## Default Entry Point

Use `/oopforge:craft` (`commands/craft.md`) as the single OOPforge user entry point.

`/oopforge:craft` delegates orchestration to `skills/workflow/craft.md`, reads `skills/principles/oop-discipline.md`, requires an OOP Contract before business-logic implementation, and verifies Hard Rules before completion.

- Use `/oopforge:craft` for single components, existing-domain features, domain bug fixes, and behavior-preserving refactors.
- For ambiguous or advisory requests, Craft recommends the smallest path without implementing.
- For a new domain or large feature, Craft routes into the existing Discovery → Test workflow and keeps the human checkpoints.

## Skill Path Convention

Resolve the OOPforge pack root in order: `$OOPFORGE_HOME` → `~/.oopforge` → repository root (when developing this pack).

Skill files live at `{pack}/skills/...`. Do **not** use legacy `skills/oopforge/...` paths. See `scripts/path-convention.md`.

## Project Configuration (target project `AGENTS.md`)

Optional single-line directives the target project can set to control OOPforge behavior:

| Directive | Effect |
|---|---|
| `OOPforge work dir: <path>` | Override the continuity work dir (default `.craft/`). |
| `OOPforge continuity: off` | Disable automatic `.craft/` work-doc creation. |

By default, continuity work docs are **auto-created (opt-out)** for execution tasks (feature/refactor/bugfix); advisory and tiny tasks never create one. See `skills/workflow/continuity.md`.

## Skill Routing

Use this table to decide **which skill to read first**. Workflow stage always wins over ad-hoc coding.

| Workflow stage | Goal | Read first |
|---|---|---|
| Craft (entrypoint) | Select and execute the smallest OOP path, or recommend only for advisory requests | `skills/workflow/craft.md` + `skills/principles/oop-discipline.md` |
| Discovery | Glossary, contexts, actors | `skills/workflow/discovery.md` |
| Design | Use-case signatures, aggregates | `skills/workflow/design.md` + `skills/oop/domain-model.md` |
| Delivery Plan | Scope, order, tests, risks | `skills/workflow/delivery-plan.md` |
| Skeleton | Packages, empty types | `skills/workflow/skeleton.md` + `skills/skeleton/backend-skeleton.md` (stack via `skills/lang/backend-stack.md`) |
| Implement | One use case + tests | `skills/workflow/implement.md` + `skills/oop/use-case-boundary.md` |
| Test | Unit / integration / E2E | `skills/workflow/test.md` |
| Refactor | Behavior-preserving cleanup | `skills/workflow/refactor.md` |
| Continuity | Resume work across sessions | `skills/workflow/continuity.md` |
| Code review | Detect rule violations | Hard Rules below + `examples/calculator-java-hexagonal/` |

### Task → skill (within a stage)

| Task | Skill |
|---|---|
| Aggregate, Value Object, Domain Event | `skills/oop/domain-model.md` |
| Use case / application service / Repository port | `skills/oop/use-case-boundary.md` |
| Read/write split, complex query off the domain (CQRS) | `skills/oop/cqrs.md` |
| Backend stack selection | `skills/lang/backend-stack.md` |
| Backend package structure / skeleton | `skills/skeleton/backend-skeleton.md` |

### Harness setup

| Harness | Guide |
|---|---|
| Codex | `docs/codex.md` |
| Claude Code | `docs/claude-code.md` |
| Cursor | `docs/cursor.md` |

Reference implementation: [examples/README.md](examples/README.md) — `calculator-java-layered`, `calculator-java-hexagonal`, `calculator-python-layered`, `calculator-python-hexagonal`, `calculator-python-hexagonal-cqrs` (same calculator domain, different architectures).

## Skill Selection

Before changing behavior, read the relevant skill file:

- Domain model: `skills/oop/domain-model.md`
- Use-case boundary: `skills/oop/use-case-boundary.md`
- Backend stack selection: `skills/lang/backend-stack.md`
- Backend skeleton structure: `skills/skeleton/backend-skeleton.md`
- Craft execution mode: `skills/workflow/craft.md` + `skills/principles/oop-discipline.md`
- Craft playbooks: `skills/playbooks/feature.md` · `skills/playbooks/bug-fix.md`
- Delivery planning: `skills/workflow/delivery-plan.md`
- Testing: `skills/workflow/test.md`
- Refactoring existing or external code: `skills/workflow/refactor.md`
- Anti-patterns: `skills/antipatterns/flat-package.md`
- Resuming work across sessions (persist + restore context): `skills/workflow/continuity.md`
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

### Layer layout (layered / 3-tier)

- **Each layer is its own package/folder** — `controller/`, `service/`, `repository/`, `domain/`. Splitting a single folder by filename suffix only (`*Controller`, `*Service`, `*Repository`) is a violation.
- **Controller/Router must not call Repository directly** — go through a Service.
- After skeleton, list the directory tree and confirm the layer folders exist with the right file types. See `skills/skeleton/backend-skeleton.md` self-check.
- Enforced in CI by `scripts/ci/archlint.py` (`.github/workflows/arch-lint.yml`) — violations block the PR.

### CQRS (when adopted)

- **Query side has no side effects** — read paths must not mutate state.
- **Command side returns no read-shaped data** — return an ID or void, not a query DTO.
- Checkable via `scripts/ci/archlint.py cqrs <root>`.

## Repository Discipline

- Do not add runtime dependencies for installer scripts unless there is no simpler shell-based alternative.
- Update `CHANGELOG.md` for user-visible changes.
- When changing install behavior, verify with a clean temporary `HOME`.
- Do not claim a harness integration works until documented setup steps and a clean-session smoke test prove it. For Cursor, verify `cursor-agent --plugin-dir` loads skills before documenting.

## What Not To Do

- Do not merge workflow stages to save time.
- Do not add framework annotations or infrastructure concerns to domain examples.
- Do not create mega-prompts, mega-skills, or broad abstractions without evidence.
- Do not mix refactoring with feature changes; use `workflow-refactor` only for behavior-preserving cleanup.
