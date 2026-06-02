# Step 3 — Skeleton

[English](./03-skeleton.md) · [한국어](./03-skeleton.ko.md) · [日本語](./03-skeleton.ja.md) · [中文](./03-skeleton.zh.md)

> **包结构 + 空类型。** 业务逻辑仅 `NotImplementedError` / `UnsupportedOperationException`。

技能: `{pack}/skills/workflow/skeleton.md`

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

## 检查点

提问: *"Skeleton 是否 OK，先实现哪个用例?"*

下一步: [04-implement-java.zh.md](./04-implement-java.zh.md) · [04-implement-python.zh.md](./04-implement-python.zh.md)
