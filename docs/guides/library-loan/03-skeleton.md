# Step 3 — Skeleton

[English](./03-skeleton.md) · [한국어](./03-skeleton.ko.md) · [日本語](./03-skeleton.ja.md) · [中文](./03-skeleton.zh.md)

> **Packages + empty types.** Business logic is `NotImplementedError` / `UnsupportedOperationException` only.

Read skills: `{pack}/skills/workflow/skeleton.md`

- Java: `{pack}/skills/lang/java/spring-hexagonal-layout.md` → command: `/oopforge:skeleton java-spring`
- Python: `{pack}/skills/lang/python/clean-fastapi-layout.md` → command: `/oopforge:skeleton python-fastapi`

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

## Checkpoint

Ask: *"Skeleton looks good — which use case should we implement first?"*

Next: [04-implement-java.md](./04-implement-java.md) · [04-implement-python.md](./04-implement-python.md)
