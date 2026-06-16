---
name: workflow-implement
description: The step after Skeleton. Implement one use case at a time, with tests.
tags: [workflow, ddd]
stability: stable
---

# Workflow — Implement

## When to use
When Skeleton is done. **One use case = one Implement cycle.**
Do not implement several use cases at once.

## Checklist (per use case)
- [ ] Implement domain model methods + unit tests
- [ ] Implement the use case class (orchestration)
- [ ] Implement port adapters (only what is needed)
- [ ] Implement the inbound adapter (Controller, etc.)
- [ ] At least one integration test
- [ ] Pass human code review

## Implementation order (inside-out)

```
1. Domain model methods + unit tests   <- start here
2. Use case class
3. Outbound port adapter (Repository implementation, etc.)
4. Inbound adapter (REST Controller, etc.)
5. Integration test
```

Writing the domain first prevents leaking into the framework.

## Just before writing: climb the ladder

Before writing each piece, climb the `skills/principles/oop-discipline.md` #7
ladder — if the standard library, a framework default, or an existing dependency
does it, do not hand-write it. But domain structure (Aggregate boundaries,
invariants, ports) is essential complexity and is not cut, and trust-boundary
validation, data loss, and security are not skipped. Leave a marker with the
upgrade path for anything you intentionally defer.

## Test priority

| Kind | Required? | Example tools |
|---|---|---|
| Domain unit test | **required** | JUnit, pytest |
| Use-case test (port mock) | **required** | Mockito, unittest.mock |
| Integration test (incl. DB) | **required** | Testcontainers, pytest-docker |
| E2E | optional | RestAssured, httpx |

## Prohibited
- **No implementing multiple use cases at once** — one at a time, next after merge.
- **No committing domain logic without tests**
- **No annotations on the domain** — `@Entity`, `@Component`, etc. live only in the infrastructure layer
- **Resist the urge to add CRUD methods** — use business verbs only
- **TDD not required, tests required** — order is free, existence is mandatory

## Definition of Done
- Unit tests + integration tests pass
- At least one code reviewer
- Change summary in `CHANGELOG` or the PR description
- Merge before moving to the next use case

## Next step
Merge the completed use case -> repeat the Implement cycle for the next use case.
When all use cases are done -> domain-level retrospective.
