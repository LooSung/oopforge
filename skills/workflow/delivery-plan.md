---
name: workflow-delivery-plan
description: Consolidate everything from requirement confirmation to implementation order, tests, review, and release risks into one execution plan.
tags: [workflow, planning, delivery]
stability: stable
---

# Workflow — Delivery Plan

## When to use
After Discovery/Design, or when requirements have arrived but the scope and contract are too unclear to implement directly.
Merge the existing tech spec and kickoff docs into **one execution plan**.

## Purpose
- Make clear what to build.
- Make clear what not to build.
- Agree on the order to implement and verify.
- Surface the risks to check before review, commit, merge, and release.

## Checklist
- [ ] Write a Problem 1-Pager: Background, Problem, Goal, Non-goals, Constraints
- [ ] Define use cases and success criteria
- [ ] If there is an external contract (API/CLI/UI), define inputs/outputs/errors
- [ ] Separate the responsibilities of domain model, application service, ports, and adapters
- [ ] Break the implementation order into small steps
- [ ] Test strategy: unit, integration, E2E checkpoints
- [ ] Review checklist: file size, layer dependencies, domain rules
- [ ] Draft commit/push/MR/release notes
- [ ] Rollback or revert strategy

## Output

Save to `docs/delivery-plan.md` or `docs/<domain>/delivery-plan.md`:

```markdown
# <Feature> — Delivery Plan

## Problem 1-Pager
- Background:
- Problem:
- Goal:
- Non-goals:
- Constraints:

## Scope
- In:
- Out:

## Contract
- Use cases:
- Inputs:
- Outputs:
- Errors:

## Responsibility Map
| Concern | Domain | Application | Infrastructure | Interfaces |
|---|---|---|---|---|
|  |  |  |  |  |

## Implementation Order
1. Domain model / value objects
2. Application use case
3. Ports and adapters
4. Interface layer
5. Tests and E2E checks

## Test Plan
- Unit:
- Integration:
- E2E:

## Review / Merge / Release
- Review checklist:
- Commit summary:
- MR notes:
- Deploy risks:
- Rollback:

## Open Questions
- 
```

## Prohibited
- **Do not write it like an implementation result report** — organize what is to be done.
- **Do not write an unconfirmed contract as if confirmed** — if unknown, leave it in Open Questions.
- **Do not force company/framework-specific rules** — follow only the rules in the project `AGENTS.md`.
- **Do not list long file paths** — responsibility boundaries and order matter more.

## Next step
After user approval -> `workflow-skeleton`, or a small `workflow-implement` directly.
