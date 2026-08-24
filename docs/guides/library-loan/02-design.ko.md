# Step 2 — Design

[English](./02-design.md) · [한국어](./02-design.ko.md)
> **시그니처만.** 메서드 본문·프레임워크 코드 작성 금지.

스킬: `{pack}/skills/workflow/design.md`, `{pack}/skills/oop/domain-model.md`

출력 저장 위치: `docs/library/design.md`

---

## 예시 출력

```markdown
# Library Lending — Design

## Use Cases
- `borrowBook(memberId, bookId): LoanId`
- `returnBook(loanId): void`

## Aggregate: Loan (root)

- **Identity**: `LoanId`
- **State**: `memberId`, `bookId`, `borrowedAt`, `status`
- **Invariants**:
  - 이미 대출 중인 Book은 다시 대출 불가
  - RETURNED 상태에서 returnBook 불가
- **Methods** (시그니처만):
  - `Loan.borrow(loanId, memberId, bookId): Loan`
  - `loan.returnBook(): void`

## Domain Events
- `BookBorrowed(loanId, memberId, bookId, borrowedAt)`
- `BookReturned(loanId, returnedAt)`

## Ports (인터페이스만)
- `LoanRepository.findById(id): Loan?`
- `LoanRepository.findActiveLoanByBookId(bookId): Loan?`
- `LoanRepository.save(loan): void`
- `DomainEventDispatcher.dispatch(events): void`
```

---

## 체크포인트

질문: *"Delivery Plan을 세우기 전에 이 Design이 행동과 경계를 올바르게
담았나요?"*

다음: [03-delivery-plan.ko.md](./03-delivery-plan.ko.md)
