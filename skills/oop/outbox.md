---
name: oop-outbox
description: Commit the state change and the outgoing event in one transaction, then deliver from that record — preventing ghost and lost events.
tags: [oop, ddd, transaction, messaging, outbox]
stability: stable
---

# OOP — Transactional Outbox

## When to use

Use this when one use case must **change state and tell the outside world** —
publish to a broker, notify another service, enqueue a job. That is two writes
to two systems with one commit between them, and no transaction spans both.

Pairs with `skills/oop/transaction-boundary.md` (one Aggregate per TX).

## The failure it prevents

Without an outbox, whichever write goes second can fail alone:

| Order of operations | Failure | Result |
|---|---|---|
| publish, then commit | commit rolls back | **ghost event** — consumers act on an order that was never placed |
| commit, then publish | broker/network fails | **lost event** — payment never charged, no error anywhere |
| publish inside the TX | broker is slow | TX held open across an external call; locks and timeouts |

Retry does not fix this. A retry after a crash cannot know which of the two
writes already happened.

## Entry criteria (do not adopt unless at least one holds)

- [ ] A use case writes domain state **and** something outside the DB must learn about it.
- [ ] A consumer's correctness depends on that message arriving.
- [ ] Losing or duplicating the message would be a business incident, not a nuisance.

If nothing outside the transaction consumes the event, do not build an outbox.
In-process Domain Event dispatch is the smaller rung
(`skills/principles/oop-discipline.md` #7).

## Rule

**One transaction, one store.** Write the Integration Event as a row in the
same database and transaction as the Aggregate save. Nothing else publishes.

```text
placeOrder TX:
  Order.place(...)          -> orders.save(order)
                            -> outbox.append(OrderPlaced)   # same TX
  commit                                                    # both or neither

relay (separate process, no TX with the above):
  read unpublished rows -> publish to broker -> mark published
```

The commit is now the only decision point. After it, the message exists and
delivery is a retryable transport problem instead of a consistency problem.

## The outbox row is not a second Aggregate

`transaction-boundary` still holds: **one Aggregate modified per transaction.**
The outbox row is a technical record of a decision that Aggregate already made,
not a second consistency boundary. It has no invariants, no behavior, and no
one loads it as a domain object.

If you find yourself adding business rules to outbox rows, you are building a
workflow engine. That responsibility is outside this delivery mechanism.

## Where each piece lives

| Piece | Layer | Note |
|---|---|---|
| Domain Event | domain | recorded by Aggregate behavior; no framework imports |
| Integration Event mapping | application | external contract derived only when needed |
| Appending it | application service | via a required port, inside the use case's TX |
| `OutboxPort` / `OutboxRepository` | application (required port) | interface only |
| Table write | adapter / infrastructure | same DataSource/session as the Aggregate repository |
| Relay or CDC | infrastructure | separate process; never imported by the domain |

The save/pop/dispatch lifecycle and handler boundary belong to
`skills/oop/domain-events.md`. This skill owns the atomic outbox append and
delivery after commit.

## Row shape (keep it minimal)

```text
id            — outbox row id
aggregate_id  — ordering key, and where the event came from
event_type    — OrderPlaced
schema_version — external contract version
payload       — serialized facts
occurred_at   — when the domain decided, not when it shipped
published_at  — null until the relay confirms
attempts      — for backoff and poison detection
```

Store the facts, not a pointer. A payload that says "read order 42 for details"
gives the consumer whatever the order looks like *now*, not when it happened.

## Delivery: relay or CDC

| | Polling relay | CDC (log tailing) |
|---|---|---|
| How | worker queries unpublished rows on an interval | connector reads the DB write-ahead log |
| Cost | code you own; no new infrastructure | Debezium-class pipeline to run and operate |
| Latency | interval-bound | near real time |
| Choose when | **default** | you already run log-based capture |

Default to the relay. CDC is new infrastructure, and the ladder says do not add
it until an existing pipeline makes it the cheaper rung.

## At-least-once, and what that costs the consumer

A crash between publish and `mark published` re-sends the message. This is
inherent — do not claim exactly-once.

- Carry the outbox row ID as `message_id`; consumer idempotency and schema
  compatibility follow `skills/oop/domain-events.md`.
- **Ordering holds per `aggregate_id` only.** Do not design for global order.
- Mark rows published **after** the broker acknowledges, never before.
- Cap `attempts` and move poison rows aside; a stuck row must not block the rest.

## OOP Contract additions

For a use case that publishes, add these lines to Craft's OOP Contract:

```markdown
Publishes: <event name — which consumer needs it>
Outbox port: <port name, appended inside the use case TX>
Delivery: relay | CDC
Consumer idempotency: <what the consumer dedupes on>
```

## Checklist

- [ ] Transaction Boundary still names exactly one Aggregate; the outbox append rides that same commit.
- [ ] No broker, HTTP, or queue call happens between transaction start and commit.
- [ ] The domain layer imports nothing from the broker or the relay.
- [ ] The outbox adapter shares the Aggregate repository's connection/session — not a second one.
- [ ] The Integration Event follows the message contract in `skills/oop/domain-events.md`.
- [ ] Rows are marked published only after broker acknowledgement.
- [ ] A test proves a rolled-back use case leaves **no** outbox row.
- [ ] A test proves a failed publish leaves the row unpublished and retryable.

## Prohibited

- **Do not publish from the domain** — follow `skills/oop/domain-events.md`.
- **Do not call the broker inside the transaction** — that reintroduces the dual write and holds locks.
- **Do not open a separate transaction or connection for the outbox insert** — one commit or none.
- **Do not delete rows at publish time** before acknowledgement; mark published, purge later.
- **Do not promise exactly-once** — deduplicate at the consumer instead.
- **Do not route internal, same-process calls through the outbox** — that is indirection, not durability.
- **Do not grow outbox rows into a workflow engine** — coordination is a separate design.

## Related

- `skills/oop/transaction-boundary.md` — one Aggregate per transaction
- `skills/oop/domain-events.md` — event lifecycle and Integration Event contract
- `skills/oop/domain-model.md` — Aggregate behavior and invariants
- `skills/oop/use-case-boundary.md` — required port, explicit transaction
- `skills/principles/oop-discipline.md` — #7 ladder, #5 reference by ID
- `skills/workflow/craft.md` — OOP Contract
