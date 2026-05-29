# OOPforge — Agent Instructions

If you are an AI coding agent working in this repository, follow OOPforge itself.

## Mission

OOPforge is a portable OOP/DDD methodology pack for coding agents.
Protect the core promise: small skills, clean domain models, explicit workflow stages, and human checkpoints.

## Required Workflow

For new domains or large features, do not jump straight to code.

1. **Discovery** — read `skills/workflow/discovery.md`; produce glossary, contexts, actors, open questions.
2. **Design** — read `skills/workflow/design.md`; produce use-case signatures, aggregate outlines, ports.
3. **Delivery Plan** — read `skills/workflow/delivery-plan.md`; align requirements, scope, implementation order, tests, and release risks.
4. **Skeleton** — read `skills/workflow/skeleton.md`; create package structure and empty interfaces/classes only.
5. **Implement** — read `skills/workflow/implement.md`; implement one use case with tests.
6. **Test** — read `skills/workflow/test.md`; run unit, integration, and E2E checks as needed.

Ask for human approval before moving from one stage to the next.

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
- Java layout: `skills/lang/java/spring-hexagonal-layout.md`
- JPA repositories: `skills/lang/java/jpa-repository.md`
- Python layout: `skills/lang/python/clean-fastapi-layout.md`
- Pydantic value objects: `skills/lang/python/pydantic-value-object.md`
- Delivery planning: `skills/workflow/delivery-plan.md`
- Testing: `skills/workflow/test.md`
- Refactoring existing or external code: `skills/workflow/refactor.md`

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

- Keep harness packaging portable: Claude and Codex are installable today; Cursor has a Phase 2 manifest only (no `install.sh` target yet); OpenCode is experimental/opt-in.
- Do not add runtime dependencies for installer scripts unless there is no simpler shell-based alternative.
- Update `CHANGELOG.md` for user-visible changes.
- When changing install behavior, verify with a clean temporary `HOME`.
- Do not claim a harness integration works until `install.sh`, `doctor.sh`, and a clean-session smoke test prove it.

## What Not To Do

- Do not merge workflow stages to save time.
- Do not add framework annotations or infrastructure concerns to domain examples.
- Do not create mega-prompts, mega-skills, or broad abstractions without evidence.
- Do not make OpenCode part of the default install path unless its integration becomes stable.
- Do not mix refactoring with feature changes; use `workflow-refactor` only for behavior-preserving cleanup.
