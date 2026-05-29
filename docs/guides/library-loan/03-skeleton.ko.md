# Step 3 — Skeleton

[English](./03-skeleton.md) · [한국어](./03-skeleton.ko.md) · [日本語](./03-skeleton.ja.md) · [中文](./03-skeleton.zh.md)

> **패키지 + 빈 타입.** 비즈니스 로직은 `NotImplementedError` / `UnsupportedOperationException` only.

스킬: `{pack}/skills/workflow/skeleton.md`

- Java: `{pack}/skills/lang/java/spring-hexagonal-layout.md` → 명령: `/oopforge:skeleton java-spring`
- Python: `{pack}/skills/lang/python/clean-fastapi-layout.md` → 명령: `/oopforge:skeleton python-fastapi`

---

## Java (Spring hexagonal)

```text
src/main/java/com/example/
└── lending/
    ├── domain/                         ← framework import 0
    │   ├── Loan.java
    │   ├── LoanId.java
    │   ├── MemberId.java
    │   ├── BookId.java
    │   ├── LoanStatus.java
    │   └── BookBorrowed.java
    ├── application/
    │   ├── provided/
    │   │   ├── BorrowBook.java
    │   │   └── ReturnBook.java
    │   ├── required/
    │   │   └── LoanRepository.java
    │   └── service/
    │       ├── BorrowBookService.java
    │       └── ReturnBookService.java
    ├── adapter/
    │   ├── web/
    │   │   ├── LoanController.java
    │   │   ├── BorrowBookRequest.java
    │   │   └── LoanResponse.java
    │   └── persistence/
    │       └── InMemoryLoanRepository.java
    └── config/
        └── LendingConfig.java
```

---

## Python (FastAPI clean layout)

```text
app/
├── domain/lending/
│   ├── model.py
│   ├── value.py
│   └── repository.py
├── application/services/lending/
│   ├── borrow_book_service.py
│   └── return_book_service.py
├── infrastructure/repositories/lending/
│   └── in_memory_loan_repository.py
└── presentation/api/lending/
    ├── loan_router.py
    └── request.py
```

---

## 체크포인트

질문: *"Skeleton 검토하고 Implement할 유스케이스를 골라주세요."*

다음: [04-implement-java.ko.md](./04-implement-java.ko.md) · [04-implement-python.ko.md](./04-implement-python.ko.md)
