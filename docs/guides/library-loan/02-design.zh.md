# Step 2 — Design

[English](./02-design.md) · [한국어](./02-design.ko.md) · [日本語](./02-design.ja.md) · [中文](./02-design.zh.md)

> **仅签名。** 不写方法体或框架代码。

技能: `{pack}/skills/workflow/design.md`, `{pack}/skills/oop/aggregate-root.md`

输出保存至: `docs/library/design.md`

---

## 示例输出

```markdown
# Library Lending — Design

## Use Cases
- `borrowBook(memberId, bookId): LoanId`
- `returnBook(loanId): void`

## Aggregate: Loan (root)

- **Identity**: `LoanId`
- **State**: `memberId`, `bookId`, `borrowedAt`, `status`
- **Invariants**:
  - 已借出的 Book 不能再次借出
  - RETURNED 状态下不能调用 returnBook
- **Methods** (仅签名):
  - `Loan.borrow(loanId, memberId, bookId): Loan`
  - `loan.returnBook(): void`

## Domain Events
- `BookBorrowed(loanId, memberId, bookId, borrowedAt)`
- `BookReturned(loanId, returnedAt)`

## Ports (仅接口)
- `LoanRepository.findById(id): Loan?`
- `LoanRepository.findActiveLoanByBookId(bookId): Loan?`
- `LoanRepository.save(loan): void`
```

---

## 检查点

提问: *"Design 是否 OK，可以进入 Delivery Plan 或 Skeleton?"*

下一步: [03-skeleton.zh.md](./03-skeleton.zh.md)
