---
name: antipattern-god-aggregate
description: The anti-pattern where one Aggregate owns unrelated invariants, lifecycles, or half the domain model.
tags: [antipattern, aggregate, boundary]
stability: experimental
---

# Anti-pattern — God Aggregate

## Symptom

A single Aggregate Root grows into a catch-all: customer profile, payments,
shipments, inventory, and notifications all hang off one root and one transaction.

```text
Order
  ├── lines, pricing, coupons
  ├── payment capture + refunds
  ├── warehouse reservation
  └── customer loyalty points
```

Any change risks the whole graph; the class file approaches the 300-line Hard Rule.

## Why it is bad

- Transaction boundaries become huge; contention and surprising rollbacks increase.
- Unrelated invariants couple — a shipping fix can break payments.
- Teams cannot evolve contexts independently (early monolith Aggregate).
- Opposite of anemic: behavior exists, but the **boundary** is wrong.

## Why it happens

"Everything related to the order" modeling, fear of eventual consistency, and
agents that put every noun from the prompt onto one root for convenience.

## Correct shape

Split by **consistency need**: what must be strongly consistent together stays
in one Aggregate; the rest collaborate by ID + domain events / follow-up use cases.

```text
Order (lines, place/cancel)          // own lifecycle
Payment (capture/refund) by orderId  // separate Aggregate
Shipment (dispatch) by orderId       // separate Aggregate
```

See `skills/oop/transaction-boundary.md` — one Aggregate modified per transaction.

## Detection

- One Aggregate file dominates the domain package (near/over 300 lines).
- Root references other Aggregates as objects, not IDs.
- Use cases always load the same mega-root to change unrelated fields.
- Invariants in the OOP Contract span multiple business capabilities.

## Remediation

1. List invariants; cluster those that must commit together.
2. Extract new Aggregates; replace object refs with IDs.
3. Replace in-proc multi-entity updates with a use case sequence or domain events
   (eventual consistency) when clusters do not share a transaction.
4. Keep each Aggregate testable in isolation; update Craft Contract boundaries.

## Related

- `skills/oop/transaction-boundary.md` — one Aggregate per transaction
- `skills/oop/domain-model.md` — Aggregate Root checklist
- `skills/antipatterns/anemic-domain.md` — opposite failure mode
- `skills/workflow/refactor.md` — behavior-preserving splits
