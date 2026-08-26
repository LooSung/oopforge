---
name: oopforge
description: Use OOPforge when building, refactoring, consulting on, or testing a backend service, REST/HTTP API, or business feature in Java or Python — including DDD/OOP modeling, layered or hexagonal/clean architecture, CQRS, or the Craft, Refactor, Consult, and Test workflows.
license: MIT
compatibility: Claude Code, Codex CLI, Cursor Agent, and Agent Skills-compatible clients with access to the complete OOPforge pack.
stability: stable
---

# OOPforge

When an OOPforge invocation contains `OOPFORGE_ACTIVATION_PROBE`, output these
three lines and stop without reading supporting files:

```text
OOPFORGE_LOADED
Assumptions
OOP Contract
```

Use this skill when the user asks for OOPforge, DDD/OOP modeling, clean or hexagonal architecture, domain-first implementation, or the `/oopforge:craft` prompt — and also for everyday backend build requests in Java/Python (e.g. "make a calculator", "build an order API"), so they are governed instead of free-formed.

**Stack scope:** OOPforge targets **Java Spring** and **Python FastAPI** backends only. If a request leaves the language unspecified, steer the user to a supported stack rather than picking one silently. If it targets an unsupported stack (JavaScript/TypeScript, frontend, mobile, CLI), tell the user OOPforge does not apply there; only build it as a plain (non-OOPforge) task if the user explicitly insists. See `lang/backend-stack.md`.

## Command Routing

Treat **`/oopforge:craft`** as the default OOPforge entry point on **Claude Code**. Use **`/oopforge:refactor`** for behavior-preserving cleanup, **`/oopforge:consult`** for advisory work, and **`/oopforge:test`** to verify, write, or strengthen tests without changing production behavior.

On **Codex CLI**, do not type OOPforge `/` commands at the composer — Codex reserves `/` for built-ins. Use `/skills` or `$oopforge` → **oopforge**, then `craft: …`, `refactor: …`, `consult: …`, or `test: …` without a leading `/`.

On **Cursor Agent CLI**, use the explicit local-plugin or project-local skill
setup documented in `../docs/setup/cursor.md`, then use natural-language intents
such as `Use OOPforge craft: …`, `Use OOPforge refactor: …`, `Use OOPforge
consult: …`, or `Use OOPforge test: …`. OOPforge `/` commands are not Cursor
headless entry points.

## Project vs pack (paths)

- **Pack** — `~/.oopforge` or `$OOPFORGE_HOME`: skills, commands, examples. Not where user app code lives.
- **Target project** — the repo the user is working on; start the agent **from this directory** (`cd your-project && codex`).
- **OOPforge maintenance** — if the user asks to change OOPforge itself, the pack repository is the work target; do not reject it as the wrong directory.
- User file paths (`docs/foo.md`, `@path`, absolute paths) resolve against the confirmed work target. For app work this is the target project, never the pack. If missing, ask for an absolute path — do not search only under `~/.oopforge`.

| Prompt | Read first | Output |
|---|---|---|
| `/oopforge:craft …` (Claude) or `Use OOPforge craft: …` (Codex/Cursor) | `workflow/craft.md` + `principles/oop-discipline.md` | select the smallest OOP path; execute unless advisory only |
| `/oopforge:refactor …` (Claude) or `Use OOPforge refactor: …` (Codex/Cursor) | `workflow/craft.md` + `workflow/refactor.md` + `principles/oop-discipline.md` | preserve behavior while improving one structural decision |
| `/oopforge:consult …` (Claude) or `Use OOPforge consult: …` (Codex/Cursor) | `workflow/consult.md` | answer, propose, review, or explicitly write one planning document without implementation changes |
| `/oopforge:test …` (Claude) or `Use OOPforge test: …` (Codex/Cursor) | `workflow/craft.md` + `workflow/test.md` | verify, write, or strengthen tests within an explicit test-only write scope |

Use Craft as the default when the user does not know which path fits. Existing Craft refactor requests remain valid for v1.x compatibility; the explicit Refactor intent narrows authorization to behavior-preserving work. Do not force the full Discovery→Test pipeline for small, focused tasks.

Natural language also works, for example: "Use OOPforge Discovery for the payment domain."

## Workflow Rules

1. Read the routed workflow file before producing output.
2. Read only the relevant OOP or language skill files needed for the task.
3. For `/oopforge:craft`, follow `workflow/craft.md`; it owns classification, OOP Contract, execution path, and verification.
4. For an explicit Refactor request, use Craft's startup and completion gates, select `workflow/refactor.md` without reclassification, and preserve behavior.
5. For Consult, follow `workflow/consult.md`; default to read-only and write one planning document only after explicit document wording.
6. For an explicit Test request, use Craft's lifecycle gates and `workflow/test.md`; never change production behavior or infer E2E.
7. Keep the normal order for new work: Discovery -> Design -> Delivery Plan -> Skeleton -> Implement -> Test.
8. Ask for human approval before moving from one workflow stage to the next.
9. Do not merge planning, implementation, and verification in a single step unless the user explicitly asks.
10. Add `workflow/production-readiness.md` only when the user explicitly asks
   about deployment, production, or operational readiness; ordinary feature
   requests never activate it.

## Supporting Skills

Core OOP:
- Domain model: `oop/domain-model.md`
- Domain Events and Integration Events: `oop/domain-events.md`
- Use-case boundary: `oop/use-case-boundary.md`
- Transaction boundary (one Aggregate per TX): `oop/transaction-boundary.md`
- Transactional Outbox (state change + event in one commit): `oop/outbox.md`
- CQRS (read/write split, medium): `oop/cqrs.md`

Backend stack and skeleton:
- Stack selection (layered or hexagonal/clean): `lang/backend-stack.md`
- Python FastAPI boundary typing and validation: `lang/python-pydantic.md`
- Package structure / skeleton: `skeleton/backend-skeleton.md`

Conditional workflow:
- Testing: `workflow/test.md`
- Production readiness (explicit opt-in only): `workflow/production-readiness.md`
- Consultation (experimental): `workflow/consult.md`

Skill maturity is recorded in `stability.json`; current harness and stack
support boundaries are defined by `../docs/reference/support-scope.md`.

Anti-patterns:
- Flat package: `antipatterns/flat-package.md`
- Anemic domain: `antipatterns/anemic-domain.md`
- Fat controller: `antipatterns/controller-fat.md`
- Repository with business logic: `antipatterns/repository-with-business-logic.md`
- God Aggregate: `antipatterns/god-aggregate.md`
