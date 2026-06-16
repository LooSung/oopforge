---
name: backend-stack
description: Choose one stack — layered or hexagonal/clean — for a Java Spring or Python FastAPI backend.
tags: [backend, stack, java, python]
stability: stable
---

# Backend Stack

## When to use

Use this when a new backend task **has not yet decided which stack to use**.
This is the stack-selection step; do not create folder structure or empty types.
Structure creation is handled by `skills/skeleton/backend-skeleton.md`.

## Supported stacks

| Stack | Architecture |
|---|---|
| `java-spring-layered` | 3-tier (Controller/Service/Repository) |
| `java-spring-hexagonal` | hexagonal (domain/application/adapter) |
| `python-fastapi-layered` | 3-tier (Router/Service/Repository) |
| `python-fastapi-clean` | clean (domain/application/infrastructure/presentation) |

## Selection criteria

| Situation | Choice |
|---|---|
| Small service, MVP, 1–2 domains | layered |
| Domain rules are complex | hexagonal/clean |
| Many external adapters | hexagonal/clean |
| Team still learning the architecture | start layered, keep the boundary rules |

Default recommendation: 2 domains or fewer + few adapters -> layered. Otherwise -> hexagonal/clean.

## Stack scope gate (pass first)

OOPforge supports **only Java Spring and Python FastAPI** backends. If a new build request leaves the language undecided or implies another stack, handle it before code.

- **Language unspecified**: do not pick arbitrarily; present only the supported stacks (Java/Python) and let the user choose.
- **Implies an unsupported stack** (JavaScript/TypeScript, frontend, mobile, shell/CLI, etc.): clearly state that OOPforge **cannot be applied** to that stack.
- If the user still insists on that stack: proceed only as a **plain (non-OOPforge) build** without OOPforge discipline (skeleton/hard rules), and state that it is outside OOPforge scope.

## Decision procedure

1. Fix the language via the scope gate above (Java Spring or Python FastAPI).
2. Pick layered or hexagonal/clean using the criteria above.
3. If ambiguous, ask the user "3-tier (layered) or hexagonal/clean?".
4. Pass one chosen stack identifier to the next step.

## CQRS variant (optional)

- CQRS is not a separate stack but a **variant layered on top of** layered/hexagonal. Entry path: `layered -> hexagonal/clean -> CQRS`.
- Introduce it only when read/write models differ greatly or complex queries pollute the domain. Application rules and entry criteria are in `skills/oop/cqrs.md`.

## OpenAPI default policy

- Every backend stack must expose OpenAPI/Swagger directly in the dev environment.
- Follow `skills/skeleton/backend-skeleton.md` for concrete tooling and folder structure.

## Prohibited

- Do not create folder structure or empty types before the stack is decided.
- Do not mix multiple stacks in one project.
- Do not force hexagonal/clean as the default without justification.
- Do not apply the OOPforge skeleton/hard rules to an unsupported stack (JS/TS, etc.). State that it does not apply first.
