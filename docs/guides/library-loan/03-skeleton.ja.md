# Step 3 — Skeleton

[English](./03-skeleton.md) · [한국어](./03-skeleton.ko.md) · [日本語](./03-skeleton.ja.md) · [中文](./03-skeleton.zh.md)

> **パッケージ + 空の型。** ビジネスロジックは `NotImplementedError` / `UnsupportedOperationException` のみ。

スキル: `{pack}/skills/workflow/skeleton.md`

- Java/Python: `{pack}/skills/skeleton/backend-skeleton.md` (stack via `{pack}/skills/lang/backend-stack.md`)

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

## チェックポイント

質問: *"Skeleton を確認し、Implement するユースケースを選んでください。"*

次: [04-implement-java.ja.md](./04-implement-java.ja.md) · [04-implement-python.ja.md](./04-implement-python.ja.md)
