# 샘플 출력 — Design: borrow-book

[English](./design-library.md) · [한국어](./design-library.ko.md) · [日本語](./design-library.ja.md) · [中文](./design-library.zh.md)

에이전트 프롬프트용 짧은 참고. 전체 가이드: [도서관 대출 가이드](../guides/library-loan/README.ko.md).

## 유스케이스

- `borrowBook(memberId, bookId): LoanId`
- `returnBook(loanId): void`

## 애그리게이트: Loan

- 식별자: `LoanId`
- 메서드: `Loan.borrow(...)`, `loan.returnBook()`
- 이벤트: `BookBorrowed`, `BookReturned`

## 포트

- `LoanRepository.findById`
- `LoanRepository.findActiveLoanByBookId`
- `LoanRepository.save`

이 단계에서는 구현 코드 없음.
