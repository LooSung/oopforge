---
name: oop-transaction-boundary
description: Keep one Aggregate modification per transaction; treat multi-Aggregate writes as a consistency design signal.
tags: [oop, ddd, transaction, aggregate]
stability: experimental
---

# OOP — Transaction Boundary

## When to use

Use this when filling **Transaction Boundary** in Craft's OOP Contract, designing
a use case that touches more than one entity, or reviewing a service that saves
several roots in one `@Transactional` / DB session.

Pairs with `skills/oop/domain-model.md` (Aggregate Root) and
`skills/antipatterns/god-aggregate.md`.

## Rule

**One transaction modifies one Aggregate instance** (one consistency boundary).

- Load that Aggregate, call its behavior, save it, commit.
- Reference other Aggregates **by ID only** — do not load and mutate them in the same commit.
- If two Aggregates must both change for one user action, that is a design signal:
  split the use case, publish a domain event, or accept eventual consistency —
  do not silently widen the transaction to "make it work".

## Checklist

- [ ] OOP Contract names exactly one Aggregate Root as the write target for this use case.
- [ ] The application service starts/commits one transaction around that Aggregate's save.
- [ ] Other Aggregates appear only as IDs (or as read-only lookups that do not save).
- [ ] Cross-Aggregate policy is either (a) a follow-up use case, (b) a domain event handler,
      or (c) an explicit saga/process later — not a second `save` in the same commit.
- [ ] Invariants asserted in tests are all owned by that one Aggregate.

## Signals you need a different boundary

| Smell | Likely move |
|---|---|
| Service saves `Order` and `Payment` together | Separate Aggregates + event or second use case |
| Transaction retries spike on unrelated data | Aggregate too large → split (`god-aggregate`) |
| "Just add this field to Order" for another capability | New Aggregate referenced by `orderId` |
| Handler updates many roots "for consistency" | Eventual consistency or process manager — not one TX |

## Correct shape

```text
placeOrder TX:
  Order.place(...) -> orders.save(order) -> commit
  // Payment / Shipment: later use cases or after OrderPlaced
```

```text
approvePayment TX:
  Payment.approve(...) -> payments.save(payment) -> commit
  // may emit PaymentApproved; Order projection updates out of band
```

## Prohibited

- Do not mutate two Aggregate roots in one transaction "for convenience".
- Do not hold DB transactions open across external HTTP calls.
- Do not use a shared unit-of-work to hide multi-Aggregate writes without documenting the choice.
- Do not merge Aggregates solely to keep a single commit (that breeds a God Aggregate).

## Related

- `skills/oop/domain-model.md` — Aggregate Root; no multi-Aggregate TX
- `skills/oop/use-case-boundary.md` — explicit transaction in the application service
- `skills/antipatterns/god-aggregate.md` — boundary too wide
- `skills/workflow/craft.md` — OOP Contract field Transaction Boundary
