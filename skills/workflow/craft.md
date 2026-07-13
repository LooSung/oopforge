---
name: workflow-craft
description: OOPforge execution orchestrator that classifies an existing backend OOP task and runs it via the smallest appropriate path.
tags: [workflow, oop, ddd]
stability: experimental
---

# Workflow — Craft

## Purpose

Run an existing backend OOP task via the smallest appropriate execution path.
The goal is not to add code.
Make domain objects own their responsibilities and keep the application service from doing more than orchestration.

## Startup procedure

0. `skills/workflow/continuity.md` Resume: if a work doc already exists, read it first and continue. If none exists and this is an **execution task (feature/refactor/bugfix)**, create `.craft/<kind>-<slug>.md` **automatically** without asking and announce it in one line. Do not create one for advisory or tiny tasks, or if `AGENTS.md` contains `OOPforge continuity: off`.
1. Confirm the **target project**. The OOPforge **pack** (`~/.oopforge`, skill paths) is not the **repo** the user works on with Craft. If `pwd` is the pack root, you are in the wrong place — confirm the agent was started from the target project.
2. When the user points to a file via `@…`, an absolute path, or a relative path, resolve it against the **target project root** (current working directory or git root). Do not look under `{pack}/docs/…` or `~/.oopforge/…`. If missing, confirm the absolute path or project root with the user.
3. Read `skills/principles/oop-discipline.md`.
4. Review the user request and the existing code.
5. Select one smallest execution path from the table below.
6. For an advisory request, only recommend a path and do not implement.
7. For an execution request, copy the checklist of the chosen skill, playbook, or workflow into your task list.
8. If you skip any step, leave a one-line reason.
9. Write the **Assumptions** block (below), then the OOP Contract, before implementing business logic.
10. Implement and test along the chosen path. Keep changes surgical (`oop-discipline` #11).
11. Verify the Hard Rules in `AGENTS.md` and the results of the tests you ran.
12. Record design decisions, verification results, **Scope drift**, and remaining risks in the completion report format. **Completion gate**: if a continuity work doc exists, do not report done before updating that doc (Status/Progress/Decisions).

## Execution-path selection

| Request signal | Execution path |
|---|---|
| Design a single Aggregate, Value Object, or Domain Event | `skills/oop/domain-model.md` |
| Design a single use case, application service, or Repository port | `skills/oop/use-case-boundary.md` |
| Add behavior, a use case, or an API to an existing domain | `skills/playbooks/feature.md` |
| Fix a business-rule error, regression, or wrong state transition | `skills/playbooks/bug-fix.md` |
| God Service, moving responsibility, removing duplication, behavior-preserving cleanup | `skills/workflow/refactor.md` |
| Read/write model split, lifting complex queries off the domain, applying CQRS | `skills/oop/cqrs.md` |
| New domain or large feature | the full existing workflow starting at `skills/workflow/discovery.md` |
| Advisory request that wants a recommendation only | recommend the smallest path and do not implement |
| Execution request but a decision is missing ("make a calculator") | fill the decision via **Ambiguity resolution** below, then select a path |

## Ambiguity resolution (before implementation)

When the intent is execution but a decisive input is empty (language, architecture, persistence, history/query = whether CQRS, supported operations/edge cases), resolve it once before code — do not interrogate; propose defaults.

1. Identify the missing decision dimensions.
2. **Language and architecture must pass the `skills/lang/backend-stack.md` scope gate.** If unspecified, steer to a supported stack (Java-Spring/Python-FastAPI); for an unsupported stack (JS/TS, etc.) state that OOPforge does not apply (plain build only if insisted).
3. For items you can set safely, **state the default** and proceed (e.g., in-memory, layered, four arithmetic operations).
4. Ask only the 1–2 questions that actually change the result (architecture/scope) (e.g., "Do you need history/queries? -> add CQRS").
5. You may offer the `examples/` calculator family (layered/hexagonal/+CQRS) as a reference menu.

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
- Verify the Hard Rules in `AGENTS.md` against the changed files.
- Confirm **Scope drift** is `none`, or list every out-of-request change with a reason.
- If broader review is needed, run the per-layer checks in `docs/reviewer-checklist.md`.
- Run the necessary tests and record the commands and results.
- For any failed or skipped verification, leave a reason and the risk.

## Completion report

```markdown
## Design Decisions
-

## Verification
- Tests:
- Hard Rules:
- Scope drift: none | <file/change — why>

## Remaining Risks
-
```

## Stage boundaries

A new domain or large feature keeps the existing Discovery -> Test stages and human approvals.
Craft does not erase these boundaries. It performs focused work on an existing domain more strictly.
