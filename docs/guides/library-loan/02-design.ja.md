# Step 2 — Design

[English](./02-design.md) · [한국어](./02-design.ko.md) · [日本語](./02-design.ja.md) · [中文](./02-design.zh.md)

> **シグネチャのみ。** メソッド本体・フレームワークコードは書かない。

スキル: `{pack}/skills/workflow/design.md`, `{pack}/skills/oop/aggregate-root.md`

出力保存先: `docs/library/design.md`

---

## 出力例

```markdown
# Library Lending — Design

## Use Cases
- `borrowBook(memberId, bookId): LoanId`
- `returnBook(loanId): void`

## Aggregate: Loan (root)

- **Identity**: `LoanId`
- **State**: `memberId`, `bookId`, `borrowedAt`, `status`
- **Invariants**:
  - 貸出中の Book は再貸出不可
  - RETURNED 状態では returnBook 不可
- **Methods** (シグネチャのみ):
  - `Loan.borrow(loanId, memberId, bookId): Loan`
  - `loan.returnBook(): void`

## Domain Events
- `BookBorrowed(loanId, memberId, bookId, borrowedAt)`
- `BookReturned(loanId, returnedAt)`

## Ports (インターフェースのみ)
- `LoanRepository.findById(id): Loan?`
- `LoanRepository.findActiveLoanByBookId(bookId): Loan?`
- `LoanRepository.save(loan): void`
```

---

## チェックポイント

質問: *"Design を確認し、Delivery Plan または Skeleton に進んでもよいですか?"*

次: [03-skeleton.ja.md](./03-skeleton.ja.md)
