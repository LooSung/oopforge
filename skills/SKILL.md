---
name: oopforge
description: Use OOPforge for DDD, OOP, layered or hexagonal/clean architecture, aggregates, value objects, ports/adapters, OpenAPI/Swagger conventions, or workflow prompts such as /oopforge:route, /oopforge:discovery, /oopforge:design, /oopforge:delivery-plan, /oopforge:skeleton, /oopforge:implement, /oopforge:test, and /oopforge:refactor.
---

# OOPforge

Use this skill when the user asks for OOPforge, DDD/OOP modeling, clean or hexagonal architecture, domain-first implementation, or any `/oopforge:*` prompt.

## Command Routing

Treat these Codex prompts as OOPforge workflow requests:

| Prompt | Read first | Output |
|---|---|---|
| `/oopforge:route ...` | `commands/route.md` (intent → minimal skill/command) | recommendation only |
| `/oopforge:discovery ...` | `workflow/discovery.md` | `docs/discovery.md` |
| `/oopforge:design ...` | `workflow/design.md` | `docs/design.md` |
| `/oopforge:delivery-plan ...` | `workflow/delivery-plan.md` | `docs/delivery-plan.md` |
| `/oopforge:skeleton ...` | `workflow/skeleton.md` + lang layout | package structure and empty types |
| `/oopforge:implement ...` | `workflow/implement.md` | one use case with tests |
| `/oopforge:test ...` | `workflow/test.md` | tests and verification results |
| `/oopforge:refactor ...` | `workflow/refactor.md` | behavior-preserving cleanup |

`/oopforge:route` is the recommended entry point — it asks intent and points to the minimal skill/command. Do not force the full Discovery→Test pipeline for small, focused tasks (single value object, repository, refactor).

Natural language also works, for example: "Use OOPforge Discovery for the payment domain."

## Workflow Rules

1. Read the routed workflow file before producing output.
2. Read only the relevant OOP or language skill files needed for the task.
3. Keep the normal order for new work: Discovery -> Design -> Delivery Plan -> Skeleton -> Implement -> Test.
4. Ask for human approval before moving from one workflow stage to the next.
5. Do not merge planning, implementation, and verification in a single step unless the user explicitly asks.

## Supporting Skills

OOP (language-agnostic):
- Aggregates: `oop/aggregate-root.md`
- Value objects: `oop/value-object.md`
- Application services: `oop/application-service.md`
- Repository ports: `oop/repository-port.md`
- Domain events: `oop/domain-event.md`
- Bounded contexts: `oop/bounded-context.md`

Layouts — pick by domain complexity (small/MVP → layered, complex → hexagonal/clean):
- Java Spring 3-tier: `lang/java/spring-layered-layout.md`
- Java Spring hexagonal: `lang/java/spring-hexagonal-layout.md`
- Python FastAPI 3-tier: `lang/python/fastapi-layered-layout.md`
- Python FastAPI clean: `lang/python/clean-fastapi-layout.md`

Python-specific patterns:
- Python aggregate: `lang/python/python-aggregate.md`
- Python domain event: `lang/python/python-domain-event.md`
- Pydantic value object: `lang/python/pydantic-value-object.md`

API contracts:
- OpenAPI/Swagger conventions: `lang/api/openapi-conventions.md`

Roadmap and direction: `../docs/roadmap.md`
