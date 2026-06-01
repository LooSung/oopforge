---
name: oopforge
description: Use OOPforge for DDD, OOP, clean architecture, hexagonal architecture, aggregates, value objects, ports/adapters, or workflow prompts such as /oopforge:discovery, /oopforge:design, /oopforge:delivery-plan, /oopforge:skeleton, /oopforge:implement, /oopforge:test, and /oopforge:refactor.
---

# OOPforge

Use this skill when the user asks for OOPforge, DDD/OOP modeling, clean or hexagonal architecture, domain-first implementation, or any `/oopforge:*` prompt.

## Command Routing

Treat these Codex prompts as OOPforge workflow requests:

| Prompt | Read first | Output |
|---|---|---|
| `/oopforge:discovery ...` | `workflow/discovery.md` | `docs/discovery.md` |
| `/oopforge:design ...` | `workflow/design.md` | `docs/design.md` |
| `/oopforge:delivery-plan ...` | `workflow/delivery-plan.md` | `docs/delivery-plan.md` |
| `/oopforge:skeleton ...` | `workflow/skeleton.md` | package structure and empty types |
| `/oopforge:implement ...` | `workflow/implement.md` | one use case with tests |
| `/oopforge:test ...` | `workflow/test.md` | tests and verification results |
| `/oopforge:refactor ...` | `workflow/refactor.md` | behavior-preserving cleanup |

Natural language also works, for example: "Use OOPforge Discovery for the payment domain."

## Workflow Rules

1. Read the routed workflow file before producing output.
2. Read only the relevant OOP or language skill files needed for the task.
3. Keep the normal order for new work: Discovery -> Design -> Delivery Plan -> Skeleton -> Implement -> Test.
4. Ask for human approval before moving from one workflow stage to the next.
5. Do not merge planning, implementation, and verification in a single step unless the user explicitly asks.

## Supporting Skills

- Aggregates: `oop/aggregate-root.md`
- Value objects: `oop/value-object.md`
- Application services: `oop/application-service.md`
- Repository ports: `oop/repository-port.md`
- Domain events: `oop/domain-event.md`
- Bounded contexts: `oop/bounded-context.md`
- Java layout: `lang/java/spring-hexagonal-layout.md`
- Python layout: `lang/python/clean-fastapi-layout.md`
