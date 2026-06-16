---
name: backend-skeleton
description: Skeleton rules for creating the standard package structure and empty types for the chosen backend stack.
tags: [backend, skeleton, java, python]
stability: stable
---

# Backend Skeleton

## When to use

Use this in the Skeleton stage to create the package structure for an **already-chosen stack**.
If there is no stack yet, pick one first via `skills/lang/backend-stack.md`.
Do not invent a per-language layout; follow the standard structure below.

## Common rules

- [ ] Keep the domain at 0 framework imports as much as possible.
- [ ] The inbound adapter handles only request/response mapping.
- [ ] The application service handles only orchestration and the transaction boundary.
- [ ] The outbound adapter handles only repository, external API, and messaging implementations.
- [ ] Do not share an API DTO, ORM entity, and domain object as one class.
- [ ] The test folder mirrors the production structure.

## Java Spring

### Layered

```text
src/main/java/com/example/order/
├── controller/
├── service/
├── repository/
├── domain/
├── config/
└── infrastructure/
```

### Hexagonal

```text
src/main/java/com/example/order/
├── domain/
├── application/
│   ├── provided/
│   ├── required/
│   └── service/
├── adapter/
│   ├── web/
│   ├── persistence/
│   └── integration/
└── config/
```

The Java API exposes `/swagger-ui` or `/v3/api-docs` via `springdoc-openapi`.
If JPA is needed, separate the domain model from the JPA entity and convert with a mapper in the adapter.

## Python FastAPI

### Layered

Split layers by **folder**, not by filename (Hard Rule). Put dependency wiring outside the layers (`app/core/`).

```text
app/calculator/
├── router/        calculator_router.py   # HTTP in/out (no repository import)
├── service/       calculator_service.py  # orchestration
├── repository/    calculation_repository.py
├── domain/        calculation.py
└── schemas/       api_models.py
app/core/dependencies.py                  # wiring
```

### Clean

```text
app/
├── domain/
├── application/
├── infrastructure/
├── presentation/
├── config/
└── shared/
```

FastAPI generates OpenAPI by default. Specify `docs_url`, `openapi_url`, tags, response model, and error schema.
By default, separate SQLAlchemy models from domain objects.

## Self-check (right after the skeleton, required)

Right after creating the structure, print the directory tree and verify and report the following yourself. Do not move to the next stage until it passes.

- [ ] **Each layer is its own folder.** For layered, `controller/ service/ repository/ domain/` exist as real folders.
- [ ] **They are not split only by filename suffix (`*Controller`, `*Service`, `*Repository`) inside one folder.** — that is a violation.
- [ ] Each file is inside its own layer folder (controller files in `controller/`).
- [ ] The test folder mirrors the production structure.

To enforce the self-check via the build (import-linter/ArchUnit), follow `skills/skeleton/lint-enforcement.md`.

Example (layered Java, passing):

```text
order/
├── controller/OrderController.java
├── service/OrderService.java
├── repository/OrderRepository.java
└── domain/Order.java
```

Violation (split only by filename in one folder — prohibited):

```text
order/
├── OrderController.java
├── OrderService.java
└── OrderRepository.java
```

## Prohibited

- Do not write method bodies. Leave `UnsupportedOperationException` or `NotImplementedError`.
- Do not cram all business rules into the service just because you chose layered.
- Do not create empty adapters or needless interfaces just because you chose hexagonal/clean.
- Do not let the controller/router call the repository directly.
- Do not let the domain import web, persistence, or framework configuration.
