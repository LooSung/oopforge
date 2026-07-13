---
name: antipattern-repository-with-business-logic
description: The anti-pattern where Repository implementations own domain judgments, policies, or multi-aggregate orchestration.
tags: [antipattern, repository, persistence]
stability: experimental
---

# Anti-pattern — Repository with Business Logic

## Symptom

Repository methods decide eligibility, apply discounts, enforce policies, or
orchestrate several Aggregates. Persistence adapters contain `if` on domain state
beyond mapping and query construction.

```text
fun saveApprovedIfEligible(order: Order) {
  if (order.total < limit && customer.isVip()) {
    order.status = APPROVED   // judgment + mutation in repository
    em.persist(order)
  }
}
```

## Why it is bad

- Persistence becomes a second domain layer; rules diverge from Aggregate methods.
- Ports stop being intention-revealing queries and turn into hidden use cases.
- Swapping storage (in-memory → SQL) forces re-implementing business rules.
- Violates use-case boundary: repository must not own transactions of meaning, only storage.

## Why it happens

"Smart DAO" habits, stuffing logic next to the query that needs the data, and
agents optimizing for fewer classes by collapsing service + repository.

## Correct shape

Repository port: load/save/find by domain language. No policy branches.

```text
orders.findOpenByCustomer(customerId)
orders.save(order)
// eligibility lives in order.approve(...) or the use case orchestration
```

Query methods may filter by **stored facts** (`findOverdue`, `findActive`) —
that is data selection, not a decision that changes invariants.

## Detection

- Repository impl mutates domain state beyond rehydration/mapping.
- Method names encode use cases (`approveAndSave`, `cancelIfAllowed`).
- Repository starts/commits business transactions or calls external APIs.
- Domain tests cannot prove a rule without the persistence adapter.

## Remediation

1. Move judgments into Aggregate behavior (or the application service if purely orchestration).
2. Rename port methods to queries/commands of persistence intent only.
3. Keep mappers dumb: row ↔ domain, no policy.
4. Add domain/use-case tests; keep repository tests for mapping and queries.

## Related

- `skills/oop/use-case-boundary.md` — Repository port rules
- `skills/oop/domain-model.md` — where invariants belong
- `skills/antipatterns/controller-fat.md` — same leak at the other edge
- `skills/oop/transaction-boundary.md` — one Aggregate per transaction
