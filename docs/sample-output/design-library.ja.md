# サンプル出力 — Design: borrow-book

[English](./design-library.md) · [한국어](./design-library.ko.md) · [日本語](./design-library.ja.md) · [中文](./design-library.zh.md)

エージェント prompt 用の短い参照。フルガイド: [図書館貸出ガイド](../guides/library-loan/README.ja.md).

## ユースケース

- `borrowBook(memberId, bookId): LoanId`
- `returnBook(loanId): void`

## アグリゲート: Loan

- 識別子: `LoanId`
- メソッド: `Loan.borrow(...)`, `loan.returnBook()`
- イベント: `BookBorrowed`, `BookReturned`

## ポート

- `LoanRepository.findById`
- `LoanRepository.findActiveLoanByBookId`
- `LoanRepository.save`

この段階では実装コードなし。
