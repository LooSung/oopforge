---
name: workflow-skeleton
description: The step after Design/Delivery Plan. Create the per-language base package structure and interface files. No business logic yet.
tags: [workflow, ddd]
stability: stable
---

# Workflow — Skeleton

## When to use
When Design and Delivery Plan are done. Before Implement.
Create **only the package structure + empty classes/interfaces**.

## Checklist
- [ ] Confirm the target stack (if none, choose via `skills/lang/backend-stack.md`)
- [ ] Read `skills/skeleton/backend-skeleton.md` first
- [ ] Create layer folders (3-tier or hexagonal/clean)
- [ ] Create aggregate/entity class skeletons (fields + empty methods)
- [ ] Value object class skeletons
- [ ] Define port interfaces / Repository interfaces (no implementations)
- [ ] Use-case/Service class skeletons (empty execute methods)
- [ ] Build-tool files (Gradle, pyproject.toml, etc.) with dependencies only
- [ ] Mirror the test folder
- [ ] **Self-check**: pass the "Self-check" in `skills/skeleton/backend-skeleton.md` — each layer its own folder, no splitting by filename suffix only in one folder

## Separate stack from layout

Keep stack selection and structure creation separate.

- If the stack is not chosen yet -> pick one via `skills/lang/backend-stack.md`.
- If the stack is decided -> follow the standard structure in `skills/skeleton/backend-skeleton.md`.

Skeleton does not invent a layout itself.

## Output

- Files with empty method signatures only
- Compiles/runs (`UnsupportedOperationException`, `NotImplementedError`, TODO)
- Test folder structure (tests may be empty)
- Record the created structure in `docs/skeleton.md` or `docs/<domain>/skeleton.md`

## Prohibited
- **No method bodies** — `throw new UnsupportedOperationException()` or `raise NotImplementedError`
- **No logic such as `if`, `for`**
- **No database schema definitions** — defer to the Implement stage
- **No layer violations** — the domain imports no other layer
- **Do not ignore the backend layout** — prefer `skills/skeleton/backend-skeleton.md` for the Java/Python base structure.

## Next step
After user approval -> `workflow-implement` (per use case)
