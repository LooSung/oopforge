---
name: workflow-continuity
description: OOPforge continuity rule that saves work context in a single doc and reads it first next session to continue. Execution tasks auto-create it by default (opt-out).
tags: [workflow, memory, continuity]
stability: experimental
---

# Workflow — Continuity

## Purpose

Let work continue even when the conversation is interrupted.
For each task, create a single Markdown doc that accumulates decisions, progress, and next steps,
and have the next session **read it first** to restore context.

## Work location

- Default: `.craft/` in the target project root.
- Override: if the target project `AGENTS.md` has the one line `OOPforge work dir: <path>`, prefer that path.
- Opt-out: if the target project `AGENTS.md` has the one line `OOPforge continuity: off`, do not create one.
- One doc per task: `<work dir>/<kind>-<slug>.md`.
  - `kind` is one of `feature`, `refactor`, `bugfix`.
  - `slug` is kebab-case. Make it deterministic so the same task always restores from the same file.
  - e.g., `.craft/feature-member-management.md`, `.craft/refactor-order-service.md`.

## Resume protocol (at task start)

1. If a work dir exists, check its listing.
2. If a doc related to the current request exists, **read it first** and continue.
3. If no related doc exists, follow **First session (auto-create)** below.
4. If the user points to a specific doc, follow that doc.

## First session (auto-create, opt-out)

When no related work doc exists, **decide creation deterministically by task kind.** Do not ask.

| Task class | Action |
|---|---|
| `feature` / `refactor` / `bugfix` (execution task) | **auto-create** then announce in one line |
| advisory · recommendation-only · tiny (e.g., a single Value Object) | do not create |
| `AGENTS.md` has `OOPforge continuity: off` | do not create |

One-line announcement on auto-create:

> Recording this task in `.craft/<kind>-<slug>.md`. (To disable, add `OOPforge continuity: off` to `AGENTS.md`.)

Creation procedure:

1. Create the work dir and the work doc.
2. If the target project `.gitignore` lacks `.craft/`, add it (personal work notes, not committed).
3. If you use an override path, make that path the `.gitignore` target.

## Work-doc format

Accumulate everything on this one page per task.

```markdown
# <Title> — <kind>

## Status
- Stage: <discovery|design|skeleton|implement|test|refactor|done>
- Updated: <date>
- Next: <one line for the next step>

## Context / Goal
- What, and why.

## Decisions (append-only)
- [<date>] <decision> — <reason>

## Progress
- [x] done
- [ ] remaining

## Open Questions / Risks
- Unknowns, risks.

## Links
- commit / PR / related code paths
```

## Update rules

- When a meaningful decision is made, **append** to `Decisions` (do not delete existing lines).
- When a work unit finishes, update `Status` and `Progress`.
- Reflect Craft's completion report (Design Decisions, Verification, Remaining Risks) in this doc.
- **Completion gate**: for a task that has a doc, do not report done before updating this doc.

## Large tasks

- A new domain or large feature may keep per-stage artifacts (`discovery.md`, `design.md`, etc.) next to the work dir.
- Even then, `<kind>-<slug>.md` remains the single entry point (anchor) that links the stage docs.

## Prohibited

- **No `.craft/` for advisory/tiny tasks** — auto-create only for execution tasks (feature/refactor/bugfix).
- **No creation when `OOPforge continuity: off`** — respect the user's opt-out.
- **No overwriting the decision log** — append only.
- **No recording sensitive info** — do not leave secrets, tokens, or personal data in the doc.
- **Do not write it as a result report** — record in-progress context and next steps.
- **Do not force committing the work dir** — gitignored by default. If team sharing is needed, the user decides.
