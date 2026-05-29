# Step 4 — Implement (Python)

[English](./04-implement-python.md) · [한국어](./04-implement-python.ko.md) · [日本語](./04-implement-python.ja.md) · [中文](./04-implement-python.zh.md)

与 Java 相同用例。**Domain: stdlib + dataclasses only.**

---

## Domain

**`value.py`**
```python
from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass(frozen=True)
class LoanId:
    value: UUID

    @staticmethod
    def generate() -> "LoanId":
        return LoanId(uuid4())


@dataclass(frozen=True)
class MemberId:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("member id must not be blank")


@dataclass(frozen=True)
class BookId:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("book id must not be blank")
```

**`model.py`**
```python
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum

from app.domain.lending.value import BookId, LoanId, MemberId


class LoanStatus(str, Enum):
    ACTIVE = "ACTIVE"
    RETURNED = "RETURNED"


@dataclass(frozen=True)
class BookBorrowed:
    loan_id: LoanId
    member_id: MemberId
    book_id: BookId
    borrowed_at: datetime


@dataclass
class Loan:
    id: LoanId
    member_id: MemberId
    book_id: BookId
    borrowed_at: datetime
    status: LoanStatus
    _events: list = field(default_factory=list, repr=False)

    @staticmethod
    def borrow(loan_id: LoanId, member_id: MemberId, book_id: BookId) -> "Loan":
        now = datetime.now(UTC)
        loan = Loan(
            id=loan_id,
            member_id=member_id,
            book_id=book_id,
            borrowed_at=now,
            status=LoanStatus.ACTIVE,
        )
        loan._record(BookBorrowed(loan_id, member_id, book_id, now))
        return loan

    def return_book(self) -> None:
        if self.status is LoanStatus.RETURNED:
            raise ValueError("loan already returned")
        self.status = LoanStatus.RETURNED

    def pop_events(self) -> list:
        published = list(self._events)
        self._events.clear()
        return published

    def _record(self, event: object) -> None:
        self._events.append(event)
```

**`repository.py`**
```python
from typing import Protocol

from app.domain.lending.model import Loan
from app.domain.lending.value import BookId, LoanId


class LoanRepository(Protocol):
    def find_by_id(self, loan_id: LoanId) -> Loan | None: ...
    def find_active_loan_by_book_id(self, book_id: BookId) -> Loan | None: ...
    def save(self, loan: Loan) -> None: ...
```

---

## Application

**`borrow_book_service.py`**
```python
from dataclasses import dataclass

from app.domain.lending.model import Loan
from app.domain.lending.repository import LoanRepository
from app.domain.lending.value import BookId, LoanId, MemberId


@dataclass(frozen=True)
class BorrowBookCommand:
    member_id: str
    book_id: str


class BorrowBookService:
    def __init__(self, loan_repository: LoanRepository) -> None:
        self._repo = loan_repository

    def handle(self, command: BorrowBookCommand) -> LoanId:
        book_id = BookId(command.book_id)

        if self._repo.find_active_loan_by_book_id(book_id) is not None:
            raise ValueError(f"book already on loan: {book_id.value}")

        loan_id = LoanId.generate()
        member_id = MemberId(command.member_id)
        loan = Loan.borrow(loan_id, member_id, book_id)

        self._repo.save(loan)
        loan.pop_events()
        return loan_id
```

---

## Infrastructure & presentation

**`in_memory_loan_repository.py`**
```python
from app.domain.lending.model import Loan, LoanStatus
from app.domain.lending.repository import LoanRepository
from app.domain.lending.value import BookId, LoanId


class InMemoryLoanRepository(LoanRepository):
    def __init__(self) -> None:
        self._store: dict[LoanId, Loan] = {}

    def find_by_id(self, loan_id: LoanId) -> Loan | None:
        return self._store.get(loan_id)

    def find_active_loan_by_book_id(self, book_id: BookId) -> Loan | None:
        return next(
            (l for l in self._store.values()
             if l.book_id == book_id and l.status is LoanStatus.ACTIVE),
            None,
        )

    def save(self, loan: Loan) -> None:
        self._store[loan.id] = loan
```

**`request.py`** — DTO (非 domain)
```python
from pydantic import BaseModel, Field


class BorrowBookRequest(BaseModel):
    member_id: str
    book_id: str = Field(min_length=1)


class LoanResponse(BaseModel):
    loan_id: str
```

**`loan_router.py`**
```python
from fastapi import APIRouter, HTTPException, status

from app.application.services.lending.borrow_book_service import (
    BorrowBookCommand, BorrowBookService,
)
from app.infrastructure.repositories.lending.in_memory_loan_repository import (
    InMemoryLoanRepository,
)
from app.presentation.api.lending.request import BorrowBookRequest, LoanResponse

_router = APIRouter(prefix="/loans", tags=["loans"])
_service = BorrowBookService(InMemoryLoanRepository())


@_router.post("", response_model=LoanResponse, status_code=status.HTTP_201_CREATED)
def borrow_book(body: BorrowBookRequest) -> LoanResponse:
    try:
        loan_id = _service.handle(
            BorrowBookCommand(member_id=body.member_id, book_id=body.book_id)
        )
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e
    return LoanResponse(loan_id=str(loan_id.value))

router = _router
```

---

下一步: [05-test.zh.md](./05-test.zh.md)
