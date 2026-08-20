---
name: oop-domain-events
description: Record domain facts in an Aggregate, dispatch them at the application boundary, and translate external messages safely.
tags: [oop, ddd, domain-event, integration-event]
stability: experimental
---

# OOP — Domain Events

## When to use

Use this when an Aggregate records a fact that another part of the system may
react to. This skill owns the event lifecycle; `skills/oop/domain-model.md`
owns the Aggregate and its invariants.

## Domain Event vs Integration Event

| | Domain Event | Integration Event |
|---|---|---|
| Meaning | A fact that happened inside the domain boundary | A message contract offered to another process or context |
| Producer | Aggregate behavior | Application handler or adapter |
| Shape | Domain language; no transport concerns | Stable envelope and versioned external schema |
| Delivery | In-process application dispatch | Transactional outbox, then relay or CDC |

A Domain Event is not automatically an Integration Event. Map it explicitly
only when an external consumer needs a contract. Do not leak domain objects,
ORM entities, or framework types into that contract.

## Record inside the Aggregate

- [ ] Record a past-tense fact only after the behavior has accepted the state change.
- [ ] Include the Aggregate ID, occurrence time, and facts known at that moment.
- [ ] Keep pending events private and expose them through a destructive
      `popEvents()` / `pullEvents()` operation that returns an immutable copy.
- [ ] Do not publish, call a handler, or depend on a broker from the Aggregate.

Recording the event and changing state are one domain decision. The Aggregate
does not decide who handles the fact or how it travels.

## Application lifecycle

For one state-changing use case:

```text
begin TX
  aggregate.behave(...)       # records Domain Event
  repository.save(aggregate)
  events = aggregate.popEvents()
  application.dispatch(events)
  outbox.append(...)           # only for mapped Integration Events
commit
relay publishes outbox rows after commit
```

The application service saves before it pops and dispatches events. If
synchronous dispatch fails before commit, the state change and any outbox rows
roll back together.

## Handler boundary

- Handlers live at the application boundary, not inside domain objects.
- A handler may invoke domain behavior through a follow-up use case.
- A handler must not mutate a second Aggregate in the source transaction.
  Each write use case keeps its own one-Aggregate transaction
  (`skills/oop/transaction-boundary.md`).
- External HTTP, broker, queue, email, or job delivery must not happen in the
  source transaction. Map to an Integration Event and append it through the
  transactional outbox (`skills/oop/outbox.md`).

## External message contract

Give every Integration Event a stable envelope:

```text
message_id
event_type
schema_version
aggregate_id
occurred_at
payload
```

- Consumers deduplicate by `message_id`; when possible, store that ID in the
  same local transaction as the business effect.
- Treat delivery as at-least-once. A handler must be safe when the same message
  arrives again.
- Version the external schema independently of domain classes.
- Keep readers for supported old versions. An upcaster converts an older
  payload to the current in-memory shape before the consumer handler runs.
- Do not rewrite an already published message to look like a newer version.

## Checklist

- [ ] The Aggregate records the Domain Event; it does not dispatch it.
- [ ] The application saves, then pops and dispatches pending events.
- [ ] Application handlers do not widen the source transaction to another Aggregate.
- [ ] Every external delivery is backed by a transactional outbox row.
- [ ] Integration Events carry a message ID and schema version.
- [ ] Consumer tests prove duplicate message IDs do not repeat the business effect.
- [ ] Compatibility tests cover each supported old version and its upcaster.

## Out of scope

This skill does not define a Saga, process manager, compensation, or
cross-Aggregate workflow. Such coordination needs a separate explicit design;
it never permits two Aggregate saves in one transaction.

## Related

- `skills/oop/domain-model.md` — Aggregate behavior and invariants
- `skills/oop/use-case-boundary.md` — application orchestration and ports
- `skills/oop/transaction-boundary.md` — one Aggregate modified per transaction
- `skills/oop/outbox.md` — durable external delivery
