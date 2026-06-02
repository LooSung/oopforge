---
name: oopforge
description: Use OOPforge for DDD, OOP, layered or hexagonal/clean architecture, aggregates, value objects, ports/adapters, OpenAPI/Swagger conventions, or the /oopforge:craft workflow prompt.
---

# OOPforge

Use this skill when the user asks for OOPforge, DDD/OOP modeling, clean or hexagonal architecture, domain-first implementation, or the `/oopforge:craft` prompt.

## Command Routing

Treat this Codex prompt as the OOPforge user entry point:

| Prompt | Read first | Output |
|---|---|---|
| `/oopforge:craft ...` | `workflow/craft.md` + `principles/oop-discipline.md` | select the smallest OOP path; execute unless advisory only |

Use `/oopforge:craft` as the single user entry point. For ambiguous or advisory requests, Forge recommends the smallest path without implementation. For execution requests, it performs the smallest coherent OOP change. Do not force the full Discovery→Test pipeline for small, focused tasks.

Natural language also works, for example: "Use OOPforge Discovery for the payment domain."

## Workflow Rules

1. Read the routed workflow file before producing output.
2. Read only the relevant OOP or language skill files needed for the task.
3. For `/oopforge:craft`, follow `workflow/craft.md`; it owns classification, OOP Contract, execution path, and verification.
4. Keep the normal order for new work: Discovery -> Design -> Delivery Plan -> Skeleton -> Implement -> Test.
5. Ask for human approval before moving from one workflow stage to the next.
6. Do not merge planning, implementation, and verification in a single step unless the user explicitly asks.

## Supporting Skills

Core OOP:
- Domain model: `oop/domain-model.md`
- Use-case boundary: `oop/use-case-boundary.md`

Backend layout:
- Java/Python layered or hexagonal/clean: `lang/backend-layout.md`

Roadmap and direction: `../docs/roadmap.md`
