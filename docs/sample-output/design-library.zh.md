# 样本输出 — Design: borrow-book

[English](./design-library.md) · [한국어](./design-library.ko.md) · [日本語](./design-library.ja.md) · [中文](./design-library.zh.md)

供 agent prompt 使用的简短参考。完整指南: [图书馆借阅指南](../guides/library-loan/README.zh.md).

## 用例

- `borrowBook(memberId, bookId): LoanId`
- `returnBook(loanId): void`

## 聚合: Loan

- 标识: `LoanId`
- 方法: `Loan.borrow(...)`, `loan.returnBook()`
- 事件: `BookBorrowed`, `BookReturned`

## 端口

- `LoanRepository.findById`
- `LoanRepository.findActiveLoanByBookId`
- `LoanRepository.save`

此阶段无实现代码。
