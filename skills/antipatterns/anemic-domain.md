---
name: antipattern-anemic-domain
description: The anti-pattern where domain objects are data bags and all business rules live in application services.
tags: [antipattern, domain, anemic]
stability: experimental
---

# Anti-pattern — Anemic Domain

## Symptom

Domain types expose getters/setters (or public fields) and hold almost no behavior.
`OrderService.approve(...)` contains the real rules: status checks, totals, eligibility.

```text
// domain: data only
order.getStatus(); order.setStatus(APPROVED);

// service: owns the rules
if (order.getStatus() != PENDING) throw ...;
order.setStatus(APPROVED);
```

## Why it is bad

- Invariants are scattered across services; a second use case bypasses them easily.
- The domain language disappears — types look like DTOs or ORM rows.
- Tests need the application layer to prove business rules.
- Violates `oop-discipline` #1 (behavior lives in the domain).

## Why it happens

CRUD-first generation, "thin domain / fat service" tutorials, and agents that treat
entities as persistence models. Mapping convenience wins over behavior ownership.

## Correct shape

Put state-changing rules on the Aggregate (or domain service only when no Aggregate owns it).

```text
order.approve(approverId);   // validates + transitions inside the Aggregate
```

The application service loads, calls behavior, saves — it does not re-implement the rule.

## Detection

- Domain classes have many getters/setters and almost no intention-revealing methods.
- Application services branch on `getStatus()` / `getType()` and then `set…`.
- Domain unit tests are empty or only cover constructors; rules are tested only via API/service tests.
- Craft OOP Contract lists invariants that appear only in a service private method.

## Remediation

1. Name the missing behavior method from the use-case verb (`approve`, `cancel`, `ship`).
2. Move invariant checks and transitions into the Aggregate; remove public setters for those fields.
3. Slim the application service to load → behavior → save → publish events.
4. Add domain unit tests for the moved rules (no framework boot).

## Related

- `skills/oop/domain-model.md` — Aggregate behavior and factories
- `skills/oop/use-case-boundary.md` — thin application service
- `skills/principles/oop-discipline.md` #1 Behavior lives in the domain
- `skills/antipatterns/god-aggregate.md` — opposite extreme (too much in one Aggregate)
