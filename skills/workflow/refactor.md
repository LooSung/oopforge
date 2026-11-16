---
name: workflow-refactor
description: Take existing or external source and clean up its structure on a behavior-preserving basis. Use to recover quality without changing functionality.
tags: [workflow, refactor, quality]
stability: stable
---

# Workflow — Refactor

Contents: When to use · Core principles · Brownfield order · One branch, one decision · Abandoning a branch · Checklist · Output · Cleanup pass (opt-in) · Prohibited · Next step

## When to use
When cleaning up the structure, names, responsibility boundaries, and duplication of existing or imported source while preserving behavior.
Not a required step of the default delivery flow but a **supporting workflow used when needed**.

## Core principles
- Do not mix functional changes with refactoring.
- First pin the current behavior with tests or reproduction scenarios.
- Change in small steps and verify often.
- Preserve public behavior, API contract, and domain rules.
- If behavior must change, that is a separate Craft job.

## Brownfield order

A new domain is designed domain-first. An **existing** system is refactored
**surface-first**, because every caller already points at the domain — moving it
first breaks everything at once, and you can no longer tell a mistake from a
ripple.

1. **Surface** — routers, controllers, schemas. Callers are explicit here, and
   the contract you must preserve becomes visible before you move anything.
2. **Application** — use cases and services, following the surface you fixed.
3. **Domain and storage** — last, once the callers above are stable.

**Move first, merge later.** When two implementations look alike, relocate them
side by side **unchanged**. Consolidating during a move mixes two decisions, and
afterwards you cannot tell which one changed behavior. Merging is a separate plan.

## One branch, one decision

A refactor branch carries exactly one boundary decision. Do not widen scope
without an explicit instruction.

- A second architecture change inside one branch is how these efforts collapse:
  the diff outgrows review and no commit is left as a safe base.
- Finish a decision before the next: verify -> commit -> merge up -> branch again.
- If a policy question is still open (who owns this data, do these two merge),
  **stop and ask**. Code stacked on an undecided policy is discarded with it.

## Abandoning a branch

Resetting a branch does not remove what it left behind. After the reset, clean
the residue — otherwise the next session inherits a half-real repository.

- **Orphan files** — checking out a discarded branch leaves files in the working
  directory. On meeting an unexplained file, run `git log --all -- <path>`
  before deciding whether it belongs.
- **Ignored paths** — work docs, local scripts, and generated artifacts survive
  any reset and now describe code that no longer exists. Reconcile or archive them.
- **Dead links** — anchors pointing into the discarded work resolve to nothing,
  and a dead link reads as "the record was lost". Fix or remove them.
- Write down **why** the attempt was abandoned before deleting it. That reason
  is usually the only thing worth keeping.

## Checklist
- [ ] State In-scope / Out-of-scope
- [ ] Name the one decision this branch carries
- [ ] Define the behavior and contract to preserve
- [ ] Write characterization tests or manual reproduction scenarios
- [ ] Work surface -> application -> domain (existing code)
- [ ] Identify responsibility-separation candidates
- [ ] Search for duplication, dead code, and ambiguous names
- [ ] Check layer-dependency violations
- [ ] Change in small steps
- [ ] After each step, verify tests/build/key scenarios
- [ ] When Live run is on (`skills/workflow/test.md`) and an endpoint is in scope, send the same requests before the first step and after the last; responses must match
- [ ] Record the change summary and remaining risks

## Output

Save to `docs/refactor-plan.md` or `docs/<domain>/refactor-plan.md`:

```markdown
# <Area> — Refactor Plan

## Scope
- In:
- Out:

## Behavior To Preserve
- Public API:
- Domain rules:
- Side effects:

## Characterization
- Tests:
- Manual scenarios:

## Refactor Steps
1.
2.
3.

## Verification
- Commands:
- Results:

## Risks
- 
```

## Cleanup pass (opt-in)

Off by default. Run it only when the user asks in this request, or the target
`AGENTS.md` has `OOPforge cleanup pass: on`. Otherwise skip it silently.

When it is on and the harness provides a diff-scoped cleanup skill (Claude Code:
`/simplify`), run it once, **after** the checklist's tests/build verification is green. It
tidies the moves you just made; it does not choose the boundary decision and
does not replace this workflow.

- Scope it to this branch's diff. Files the refactor did not touch stay untouched.
- It applies edits itself. Re-run tests and build afterwards.
- Revert any edit that changes behavior or an API contract, merges two
  implementations, or carries a second decision — the rules in **Prohibited**
  still apply to its output.
- Record what it changed in the refactor plan's Verification section.
- On but no such skill in this harness: say so in one line.

## Prohibited
- **No second decision in one branch** — widen only on an explicit instruction
- **No merging two implementations during a move** — relocate, then merge separately
- **No building on an undecided policy** — stop and ask
- **No adding new features**
- **No large structural change without tests/reproduction scenarios**
- **No changing domain rules**
- **No silently changing an existing API contract**
- **No breaking domain purity for framework convenience**

## Next step
After verification -> review, commit, push. If a functional change is needed, split it into a separate Craft job.
