---
name: backend-stack
description: Choose one stack — layered or hexagonal/clean — for a Java Spring, Python FastAPI, or experimental Kotlin Spring or TypeScript NestJS backend.
tags: [backend, stack, java, kotlin, python, typescript, nestjs]
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
| `kotlin-spring-layered` | experimental: 3-tier, Kotlin |
| `kotlin-spring-hexagonal` | experimental: hexagonal, Kotlin |
| `typescript-nestjs-layered` | experimental: 3-tier folders inside a NestJS feature module |
| `typescript-nestjs-hexagonal` | experimental: hexagonal inside a NestJS feature module |

Experimental stacks are outside the 1.x compatibility promise: say so when
offering one, and never pick one for the user. Language rules live in
`lang/kotlin-spring.md`, `lang/typescript-nestjs.md`, and
`lang/python-pydantic.md`.

## Selection criteria

| Situation | Choice |
|---|---|
| Small service, MVP, 1–2 domains | layered |
| Domain rules are complex | hexagonal/clean |
| Many external adapters | hexagonal/clean |
| Team still learning the architecture | start layered, keep the boundary rules |

Default recommendation: 2 domains or fewer + few adapters -> layered. Otherwise -> hexagonal/clean.

## Stack scope gate (pass first)

OOPforge supports **Java Spring and Python FastAPI** backends, plus experimental
**Kotlin Spring** and **TypeScript NestJS**. If a new build request leaves the
language undecided or implies another stack, handle it before code.

- **Language unspecified**: do not pick arbitrarily; offer Java Spring and Python FastAPI, mention the two experimental stacks, and let the user choose.
- **Implies an unsupported stack** (JavaScript/TypeScript backends other than NestJS, such as Express or plain Node, frontend UI, mobile, shell/CLI, etc.): clearly state that OOPforge **cannot be applied** to that stack. A Next.js app — pages, components, route handlers, server actions — belongs to Compforge.
- If the user still insists on that stack: proceed only as a **plain (non-OOPforge) build** without OOPforge discipline (skeleton/hard rules), and state that it is outside OOPforge scope.

## Decision procedure

1. Fix the language via the scope gate above.
2. Pick layered or hexagonal/clean using the criteria above.
3. If ambiguous, ask the user "3-tier (layered) or hexagonal/clean?".
4. Pass one chosen stack identifier to the next step.

## CQRS variant (optional)

- CQRS is not a separate stack but a **variant layered on top of** layered/hexagonal. Entry path: `layered -> hexagonal/clean -> CQRS`.
- Introduce it only when read/write models differ greatly or complex queries pollute the domain. Application rules and entry criteria are in `skills/oop/cqrs.md`.

## OpenAPI default policy

- Every backend stack must expose OpenAPI/Swagger directly in the dev environment.
- TypeScript NestJS: `@nestjs/swagger` reads the Zod boundary schemas (`lang/typescript-nestjs.md`).
- Follow `skills/skeleton/backend-skeleton.md` for concrete tooling and folder structure.

## Prohibited

- Do not create folder structure or empty types before the stack is decided.
- Do not mix multiple stacks in one project.
- Do not force hexagonal/clean as the default without justification.
- Do not apply the OOPforge skeleton/hard rules to an unsupported stack (JavaScript/TypeScript outside NestJS, etc.). State that it does not apply first.
