# Step 2 — Design

[English](./02-design.md) · [한국어](./02-design.ko.md)
> **Signatures only.** No method bodies or framework code.

Read skills: `{pack}/skills/workflow/design.md`, `{pack}/skills/oop/domain-model.md`

Save output to: `docs/library/design.md`

---

## Example output

```markdown
# Library Lending — Design

## Use Cases
- `borrowBook(memberId, bookId): LoanId`
- `returnBook(loanId): void`

## Aggregate: Loan (root)

- **Identity**: `LoanId`
- **State**: `memberId`, `bookId`, `borrowedAt`, `status`
- **Invariants**:
  - A Book already on loan cannot be borrowed again
  - Cannot call returnBook when status is RETURNED
- **Methods** (signatures only):
  - `Loan.borrow(loanId, memberId, bookId): Loan`
  - `loan.returnBook(): void`

## Domain Events
- `BookBorrowed(loanId, memberId, bookId, borrowedAt)`
- `BookReturned(loanId, returnedAt)`

## Ports (interfaces only)
- `LoanRepository.findById(id): Loan?`
- `LoanRepository.findActiveLoanByBookId(bookId): Loan?`
- `LoanRepository.save(loan): void`
```

---

## Checkpoint

Ask: *"Design looks good — proceed to Delivery Plan or Skeleton?"*

Next: [03-skeleton.md](./03-skeleton.md)
