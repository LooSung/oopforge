# Sample Output — Discovery: Library Loan Domain

[English](./discovery-library.md) · [한국어](./discovery-library.ko.md) · [日本語](./discovery-library.ja.md) · [中文](./discovery-library.zh.md)

Short reference for agent prompts. Full walkthrough: [library loan guide](../guides/library-loan/README.md).

## Business goal

A member borrows a book. A book already on loan cannot be borrowed again. Borrowing publishes a `BookBorrowed` event.

## Bounded contexts

- **Lending** — Loan, book availability, member eligibility
- **Catalog** — book metadata (title, author) — separate from Lending

## Core concepts

- Book, Member, Loan, LoanId, BookBorrowed

## Aggregate candidate

- **Loan** (root in Lending context)

## Key invariants

- Active loan for a book blocks another borrow
- Returned loan cannot be returned again
- Catalog referenced by ID, not embedded object

## Open questions

- Max loans per member?
- Overdue policy?
- Fixed vs variable loan period?
