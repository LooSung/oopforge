# Step 3 — Delivery Plan

[English](./03-delivery-plan.md) · [한국어](./03-delivery-plan.ko.md)
> **Agree on scope, order, tests, and risks.** Do not create production files.

Read skill: `{pack}/skills/workflow/delivery-plan.md`

Save output to: `docs/library/delivery-plan.md`

---

## Example output

```markdown
# Borrow Book — Delivery Plan

## Goal and acceptance
- A member can borrow an available book and receives a Loan ID.
- A book with an active loan is rejected.
- Borrowing records and dispatches `BookBorrowed`.

## In scope
- `borrowBook(memberId, bookId): LoanId`
- Loan Aggregate behavior and event
- Repository and event-dispatch ports
- In-memory adapter and one HTTP endpoint

## Out of scope
- Returning a book
- Durable persistence or external messaging
- Production-readiness concerns

## Delivery order
1. Create the approved Java or Python skeleton.
2. Implement Loan behavior and domain tests.
3. Implement the use case with repository and dispatcher fakes.
4. Add composition wiring and the HTTP adapter.
5. Run unit, boundary, and architecture checks.

## Risks
- Active-loan uniqueness needs a durable database constraint in production.
- In-process event dispatch is not external message delivery.
```

---

## Checkpoint

Ask: *"Does this scope and delivery order match what you want before we create
the skeleton?"*

Next: [04-skeleton.md](./04-skeleton.md)
