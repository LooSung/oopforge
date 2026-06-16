---
name: workflow-refactor
description: Take existing or external source and clean up its structure on a behavior-preserving basis. Use to recover quality without changing functionality.
tags: [workflow, refactor, quality]
stability: stable
---

# Workflow — Refactor

## When to use
When cleaning up the structure, names, responsibility boundaries, and duplication of existing or imported source while preserving behavior.
Not a required step of the default delivery flow but a **supporting workflow used when needed**.

## Core principles
- Do not mix functional changes with refactoring.
- First pin the current behavior with tests or reproduction scenarios.
- Change in small steps and verify often.
- Preserve public behavior, API contract, and domain rules.
- If something must change, it is the subject of a new delivery plan.

## Checklist
- [ ] State In-scope / Out-of-scope
- [ ] Define the behavior and contract to preserve
- [ ] Write characterization tests or manual reproduction scenarios
- [ ] Identify responsibility-separation candidates
- [ ] Search for duplication, dead code, and ambiguous names
- [ ] Check layer-dependency violations
- [ ] Change in small steps
- [ ] After each step, verify tests/build/key scenarios
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

## Prohibited
- **No adding new features**
- **No large structural change without tests/reproduction scenarios**
- **No changing domain rules**
- **No silently changing an existing API contract**
- **No breaking domain purity for framework convenience**

## Next step
After verification -> review, commit, push. If a functional change is needed, split it into `workflow-delivery-plan`.
