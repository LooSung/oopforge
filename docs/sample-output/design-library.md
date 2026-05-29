# Sample Output — Design: borrow-book

[English](./design-library.md) · [한국어](./design-library.ko.md) · [日本語](./design-library.ja.md) · [中文](./design-library.zh.md)

Short reference for agent prompts. Full walkthrough: [library loan guide](../guides/library-loan/README.md).

## Use cases

- `borrowBook(memberId, bookId): LoanId`
- `returnBook(loanId): void`

## Aggregate: Loan

- Identity: `LoanId`
- Methods: `Loan.borrow(...)`, `loan.returnBook()`
- Events: `BookBorrowed`, `BookReturned`

## Ports

- `LoanRepository.findById`
- `LoanRepository.findActiveLoanByBookId`
- `LoanRepository.save`

No implementation code at this stage.
