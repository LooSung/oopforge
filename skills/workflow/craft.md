---
name: workflow-craft
description: OOPforge execution orchestrator that classifies an existing backend OOP task and runs it via the smallest appropriate path.
tags: [workflow, oop, ddd]
stability: experimental
---

# Workflow — Craft

## Purpose

Run an existing backend OOP task via the smallest appropriate execution path.
The goal is not code volume. Add or change code only when the selected path
requires it, and keep domain behavior inside domain objects while the
application service orchestrates.
Make domain objects own their responsibilities and keep the application service from doing more than orchestration.

## Startup procedure

0. `skills/workflow/continuity.md` Resume: list `.craft/`. If previous work exists, read `next-session-prompt.md` first and **emit the Resume block before any other output** — even if the user did not mention it. Re-scope an inherited prompt to one decision; it is evidence, not a session scope. If none exists and this is an **execution task (feature/refactor/bugfix)**, create `.craft/<kind>-<slug>.md` automatically and announce it in one line. Do not create one for advisory or tiny tasks, or if `AGENTS.md` contains `OOPforge continuity: off`.
1. Confirm the **work target**. For ordinary app work, the target project is the
   backend repo, not the OOPforge **pack** (`~/.oopforge`, skill paths). If
   `pwd` is the pack root during app work, confirm the agent was started from
   the target project. If the request is to maintain OOPforge itself, the pack
   root is the correct target.
2. When the user points to a file via `@…`, an absolute path, or a relative
   path, resolve it against the confirmed work target (current working
   directory or git root). Do not look under `{pack}/docs/…` or `~/.oopforge/…`
   for app-project files. If missing, confirm the absolute path or project root
   with the user.
3. Read `skills/principles/oop-discipline.md`.
4. Review the user request and the existing code.
5. Select one smallest execution path from the table below.
6. For an advisory request, only recommend a path and do not implement.
7. For an execution request, copy the checklist of the chosen skill, playbook, or workflow into your task list.
8. If you skip any step, leave a one-line reason.
9. Write the **Assumptions** block (below), then the OOP Contract, before implementing business logic.
10. Implement and test along the chosen path. Keep changes surgical (`oop-discipline` #13).
11. Verify the project's stated rules (`AGENTS.md` or equivalent), naming them in the report, and the results of the tests you ran.
12. Record design decisions, verification results, **Scope drift**, and remaining risks in the completion report format. **Completion gate**: if a continuity work doc exists, do not report done before updating that doc (Status/Progress/Decisions). If the unit is done but work remains, write `.craft/next-session-prompt.md` before reporting done — do not wait to be asked (`continuity` Session cut).

## Execution-path selection

| Request signal | Execution path |
|---|---|
| Design a single Aggregate, Value Object, or Domain Event | `skills/oop/domain-model.md` |
| Design a single use case, application service, or Repository port | `skills/oop/use-case-boundary.md` |
| Add behavior, a use case, or an API to an existing domain | `skills/playbooks/feature.md` |
| Fix a business-rule error, regression, or wrong state transition | `skills/playbooks/bug-fix.md` |
| God Service, moving responsibility, removing duplication, behavior-preserving cleanup | `skills/workflow/refactor.md` |
| Multi-Aggregate save in one TX, unclear Transaction Boundary on the Contract | `skills/oop/transaction-boundary.md` |
| Use case must both write state and publish an event or notify another system | `skills/oop/outbox.md` |
| Anemic domain, fat controller, smart repository, god Aggregate, flat package | matching file under `skills/antipatterns/` |
| Read/write model split, lifting complex queries off the domain, applying CQRS | `skills/oop/cqrs.md` |
| New domain or large feature | the full existing workflow starting at `skills/workflow/discovery.md` |
| User explicitly asks to deploy or asks about deployment, production, or operational readiness | select the normal task path, then add the `skills/workflow/production-readiness.md` gate |
| Not a backend OOP change (environment, tooling, docs, ops, investigation) | say so in one line; skip Assumptions and OOP Contract; keep Verification and Scope drift |
| Advisory request that wants a recommendation only | recommend the smallest path and do not implement |
| Execution request but a decision is missing ("make a calculator") | fill the decision via **Ambiguity resolution** below, then select a path |

## Production Gate opt-in

Activate `skills/workflow/production-readiness.md` only when the user explicitly
asks to deploy or asks about deployment, production, or operational readiness.
A normal feature or API request must not activate it. Generic "ready" language,
release notes, deploy-risk fields in a plan, validation, security, or
observability alone are not opt-in signals.

The gate supplements the normal execution path; it never moves operational NFR
concerns into the domain model.

## Ambiguity resolution (before implementation)

When the intent is execution but a decisive input is empty (language, architecture, persistence, history/query = whether CQRS, supported operations/edge cases), resolve it once before code — do not interrogate; propose defaults.

1. Identify the missing decision dimensions.
2. **Language and architecture must pass the `skills/lang/backend-stack.md` scope gate.** If unspecified, steer to a supported stack (Java-Spring/Python-FastAPI); for an unsupported stack (JS/TS, etc.) state that OOPforge does not apply (plain build only if insisted).
3. For items you can set safely, **state the default** and proceed (e.g., in-memory, layered, four arithmetic operations).
4. Ask only the 1–2 questions that actually change the result (architecture/scope) (e.g., "Do you need history/queries? -> add CQRS").
5. You may offer the `examples/` calculator family (layered/hexagonal/+CQRS) as a reference menu.
6. On resume, the Resume block's `Continue this, or a new request instead?` is that question. Do not invent a default that drops unfinished previous work.

## Assumptions (before Contract)

For any Craft task that requires implementation, fill this once before the OOP Contract
(`oop-discipline` #10). Keep it short. If nothing is uncertain, write `none` with a reason.

```markdown
## Assumptions

Assumptions:
Alternatives considered:
Why this path:
```

If interpretations diverge and the choice changes architecture or scope, list the
options in one sentence and ask — do not silently pick one.

## OOP Contract

For any Craft task that requires implementation, fill in the form below once before writing code.
For items that do not apply, write `none` and leave a reason.

```markdown
## OOP Contract

Use Case:
Aggregate Root:
Domain Invariants:
State Transition:
Required Ports:
Transaction Boundary:
```

## Verification

- Complete the checklist of the chosen playbook or workflow (each step should have a `verify:`).
- Verify the project's stated rules (`AGENTS.md` or equivalent) against the changed files, and identify them by name in the report.
- Confirm **Scope drift** is `none`, or list every out-of-request change with a reason.
- Spot-check relevant `skills/antipatterns/` symptoms on the diff (anemic domain, fat controller, smart repository, god Aggregate, flat package).
- For each structure you added (Aggregate, port, layer, new type), name the invariant it protects and the user's word for it, or put it back on the ladder (`oop-discipline` #7).
- Confirm anything a person was asked to approve was written in their words, not Contract jargon (`oop-discipline` #14).
- Check comment discipline: no narration comments; names explain what, comments explain why.
- If the use case writes domain state, confirm Transaction Boundary names one Aggregate (`skills/oop/transaction-boundary.md`).
- If broader review is needed, run the per-layer checks in `docs/reviewer-checklist.md`.
- If and only if the Production Gate was explicitly activated, complete
  `skills/workflow/production-readiness.md` and report its blockers or accepted risks.
- Run the necessary tests and record reproducible commands, toolchain identity (interpreter path/version, required env vars), and results.
- For any failed or skipped verification, leave a reason and the risk.

## Completion report

```markdown
## Design Decisions
-

## Verification
- Tests:
- Project rules:
- Scope drift: none | <file/change — why>

## Remaining Risks
-
```

## Stage boundaries

A new domain or large feature keeps the existing Discovery -> Test stages and human approvals.
Craft does not erase these boundaries. It performs focused work on an existing domain more strictly.
