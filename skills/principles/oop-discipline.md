---
name: oop-discipline
description: Core OOPforge principles to read before backend OOP work. Fixes object responsibility, boundaries, tests, and structural learning.
tags: [oop, ddd, principles]
stability: experimental
---

# OOP Discipline

Read this before starting backend OOP work.
In the completion report, mention only the principles that actually changed a design decision.

## 1. Behavior lives in the domain

Business rules belong in the behavior methods of domain objects,
not in the controller, application service, or repository adapter.

Example: prefer `payment.approve(approverId)` over `paymentService.approve(payment)`.

## 2. Define boundaries before code

Before writing code, first write down the Aggregate Root, invariants,
state transitions, ports, and transaction boundary.

## 3. Domain knows no framework

The domain model favors the business language and rules over framework convenience.
Push technical details outside the application or adapter boundary.

## 4. Use case over CRUD

Externally exposed methods are expressed as business verbs, not CRUD.
A state-change name must reveal the user's intent, not a storage operation.

## 5. Aggregate references by ID

Reference other Aggregates by ID, not by object.
Do not tie lifecycles and invariants from beyond the boundary into one object graph.

## 6. Failing test before bug fix

Fix a bug by first writing a reproducible failing test.
Then resolve it with the smallest change.

## 7. Subtract before abstracting — the pre-write ladder

Writing code is the last resort. Before building anything, climb from the top
and stop at the first rung that holds. The lower you go, the more code you add.

```
1. Does this need to exist?      -> no: don't build it (YAGNI)
2. Standard library / language?  -> use it
3. Framework default?            -> use it (Spring/FastAPI built-ins)
4. Already-installed dependency? -> use it
5. One line / one method?        -> finish it there
6. Only then                     -> write the minimum that works
```

**Essential vs accidental.** The ladder cuts only *accidental complexity*
(needless abstraction, duplication, dead code, unused flexibility). *Essential
complexity* (Aggregate boundaries, invariants, ports, layer separation) is
deliberate structure and is not subject to the ladder.

**Earn the exemption; do not claim it.** The exemption is granted by evidence,
not by category name — anything can be called an Aggregate boundary. A structure
is essential only when you can name both:

1. the invariant it protects, in one sentence;
2. the **user's own word** for the thing it protects.

If the name is one the user never used, the structure goes back on rung 1 and
has to argue for itself. Naming is where accidental complexity enters disguised
as essential.

**Lazy, not negligent.** Trust-boundary input validation, data-loss handling,
and security are never skipped at any rung.

**Leave a marker for what you defer.** If you intentionally do the minimum,
mark the spot with what you deferred and the upgrade path — so "later" never
becomes "never".

## 8. Encode lessons in structure

When you find yourself explaining the same mistake twice, do not write more docs.
Capture it as a test, lint rule, verification script, or example.

## 9. Duplicate before the wrong abstraction

DRY removes duplication of **knowledge (rules)**, not every piece of code that
merely looks alike. The cost of undoing a wrong abstraction exceeds the cost of
keeping duplication.

- Tolerate the second duplication. **Abstract only on the third (Rule of Three).**
- **Do not share a domain model across bounded contexts.** Even when two contexts'
  concepts look alike, they evolve differently, so duplication is correct here.
- What you should actually consolidate is scattered *business rules* — pull them
  into one domain behavior method. (Rules copied across services seed God Service
  and anemic domain.)

## 10. Surface assumptions before coding

Do not silently pick one interpretation when several are plausible.
Before writing business logic, state what you are assuming, what you considered,
and why this path — then proceed or ask.

- If unsure, stop and name what is unclear.
- If alternatives exist, list them briefly; do not hide the choice.
- Prefer a simpler path when it still satisfies the request; say so.
- This complements Ambiguity resolution in Craft: defaults are fine when safe,
  but the default must be **visible**, not silent.

Essential structure (Aggregates, ports, layer separation) is still required —
surfacing assumptions does not license skipping Discovery/Design/Skeleton for
a new domain or large feature.

## 11. Evidence before cause

Before recording a cause, secure one observation that would differ if that
cause were false. Prefer mechanism over correlation; if two environments behave
differently, compare the thing you believe differs before documenting it.

## 12. Comment discipline

Do not narrate code. If a comment explains what adjacent code does, delete it
or rename/extract code until the comment is unnecessary. Keep comments only for
why, external constraints, hidden invariants, or tracked temporary decisions.

## 13. Surgical changes only

Touch only what the request requires. Match existing style; do not "improve"
adjacent code, comments, formatting, or naming while delivering the task.

- Clean up orphans **your change** created (unused imports, dead locals).
- Pre-existing dead code: mention it; do not delete it in the same change.
- Do not mix unrelated refactoring with a feature or bug fix.
- Essential structure work (new port, layer folder) is in scope when the
  chosen Craft path requires it — surgical means no *accidental* drive-by edits.

## 14. Product language at the human boundary

The OOP Contract is a contract with the agent, not a screen for a person.
Aggregate, Port, Bounded Context, and any name you invented stay in the
Contract and the code — not in what you ask someone to approve.

- Ask for approval in the user's words: what changes, for whom, what breaks.
- Introduce a new name only once the thing exists and the user needs to say
  it. Then define it in one line, and keep using their word for the rest.
- An approval of a name the person cannot check is not an approval. It is the
  cheapest way to get a wrong design blessed.
