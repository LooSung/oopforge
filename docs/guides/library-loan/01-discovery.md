# Step 1 — Discovery

[English](./01-discovery.md) · [한국어](./01-discovery.ko.md) · [日本語](./01-discovery.ja.md) · [中文](./01-discovery.zh.md)

> **No code.** Define language, boundaries, and terms only.

Read skill: `{pack}/skills/workflow/discovery.md`

Save output to: `docs/library/discovery.md` (in your project)

---

## Example output

```markdown
# Library — Discovery

## Glossary
- **Book**: A physical book held by the library. Identified by unique ISBN.
- **Member**: A registered member with borrowing privileges.
- **Loan**: The fact that a Member borrowed a specific Book. Ends on return.
- **LoanId**: Value object identifying a Loan.

## Bounded Contexts
1. **Lending** — Loan, Book (availability), Member (eligibility)
2. **Catalog** — Book metadata (title, author) — separate from Lending

## Aggregate Candidates
- Lending: `Loan` (root)
- Book availability handled via separate lookup within Lending context

## Actors / External
- Member (web client)
- Catalog Service (external — verify book exists)

## Non-Functional
- Borrow processing is synchronous, p99 under 300ms
- Concurrent borrow requests for same book → only one succeeds (optimistic lock or unique constraint)

## Open Questions
- Is there a max loans per member?
- Overdue policy — block further borrows?
- Fixed return deadline or varies by book type?
```

---

## Checkpoint

Ask: *"Discovery looks good — proceed to Design?"*

Next: [02-design.md](./02-design.md)
