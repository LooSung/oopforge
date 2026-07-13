---
name: oopforge
description: Use OOPforge when building or changing a backend service, server, REST/HTTP API, or business app/feature in Java or Python — including vague build prompts like "make a calculator" or "build an order service" — and for DDD/OOP modeling, layered or hexagonal/clean architecture, aggregates, value objects, ports/adapters, CQRS, OpenAPI/Swagger, or the /oopforge:craft workflow prompt.
---

# OOPforge

Use this skill when the user asks for OOPforge, DDD/OOP modeling, clean or hexagonal architecture, domain-first implementation, or the `/oopforge:craft` prompt — and also for everyday backend build requests in Java/Python (e.g. "make a calculator", "build an order API"), so they are governed instead of free-formed.

**Stack scope:** OOPforge targets **Java Spring** and **Python FastAPI** backends only. If a request leaves the language unspecified, steer the user to a supported stack rather than picking one silently. If it targets an unsupported stack (JavaScript/TypeScript, frontend, mobile, CLI), tell the user OOPforge does not apply there; only build it as a plain (non-OOPforge) task if the user explicitly insists. See `lang/backend-stack.md`.

## Command Routing

Treat **`/oopforge:craft`** as the OOPforge user entry point on **Claude Code** (installed slash command).

On **Codex CLI**, do not type `/oopforge:craft` at the composer — Codex reserves `/` for built-in commands. Use `/skills` or `$oopforge` → **oopforge**, then `craft: …` (no leading `/`).

On **Cursor Agent CLI** (with `--plugin-dir`), use the plugin slash command like Claude: `/oopforge:craft …`.

## Project vs pack (paths)

- **Pack** — `~/.oopforge` or `$OOPFORGE_HOME`: skills, commands, examples. Not where user app code lives.
- **Target project** — the repo the user is working on; start the agent **from this directory** (`cd your-project && codex`).
- User file paths (`docs/foo.md`, `@path`, absolute paths) resolve against the **target project**, never against the pack. If missing, ask for an absolute path — do not search only under `~/.oopforge`.

| Prompt | Read first | Output |
|---|---|---|
| `/oopforge:craft …` (Claude) or `Use OOPforge craft: …` (Codex/Cursor) | `workflow/craft.md` + `principles/oop-discipline.md` | select the smallest OOP path; execute unless advisory only |

Use `/oopforge:craft` as the single user entry point. For ambiguous or advisory requests, Craft recommends the smallest path without implementation. For execution requests, it performs the smallest coherent OOP change. Do not force the full Discovery→Test pipeline for small, focused tasks.

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
- Transaction boundary (one Aggregate per TX): `oop/transaction-boundary.md`
- CQRS (read/write split, medium): `oop/cqrs.md`

Backend stack and skeleton:
- Stack selection (layered or hexagonal/clean): `lang/backend-stack.md`
- Package structure / skeleton: `skeleton/backend-skeleton.md`

Anti-patterns:
- Flat package: `antipatterns/flat-package.md`
- Anemic domain: `antipatterns/anemic-domain.md`
- Fat controller: `antipatterns/controller-fat.md`
- Repository with business logic: `antipatterns/repository-with-business-logic.md`
- God Aggregate: `antipatterns/god-aggregate.md`

Roadmap and direction: `../docs/roadmap.md`
