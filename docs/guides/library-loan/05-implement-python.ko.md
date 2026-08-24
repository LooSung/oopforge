# 5단계 — Implement (Python)

[English](./05-implement-python.md) · [한국어](./05-implement-python.ko.md)
Java와 동일한 유스케이스. **Domain: stdlib + dataclasses only.**

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


@dataclass(frozen=True)
class Loan:
    id: LoanId
    member_id: MemberId
    book_id: BookId
    borrowed_at: datetime
    status: LoanStatus
    _events: tuple[object, ...] = field(
        default_factory=tuple, init=False, repr=False, compare=False
    )

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
        object.__setattr__(self, "status", LoanStatus.RETURNED)

    def pop_events(self) -> tuple[object, ...]:
        published = self._events
        object.__setattr__(self, "_events", ())
        return published

    def _record(self, event: object) -> None:
        object.__setattr__(self, "_events", (*self._events, event))
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

**`domain_events.py`**
```python
from typing import Protocol


class DomainEventDispatcher(Protocol):
    def dispatch(self, events: tuple[object, ...]) -> None: ...
```

**`borrow_book_service.py`**
```python
from dataclasses import dataclass

from app.application.domain_events import DomainEventDispatcher
from app.domain.lending.model import Loan
from app.domain.lending.repository import LoanRepository
from app.domain.lending.value import BookId, LoanId, MemberId


@dataclass(frozen=True)
class BorrowBookCommand:
    member_id: str
    book_id: str


class BorrowBookService:
    def __init__(
        self,
        loan_repository: LoanRepository,
        event_dispatcher: DomainEventDispatcher,
    ) -> None:
        self._repo = loan_repository
        self._events = event_dispatcher

    def handle(self, command: BorrowBookCommand) -> LoanId:
        book_id = BookId(command.book_id)

        if self._repo.find_active_loan_by_book_id(book_id) is not None:
            raise ValueError(f"book already on loan: {book_id.value}")

        loan_id = LoanId.generate()
        member_id = MemberId(command.member_id)
        loan = Loan.borrow(loan_id, member_id, book_id)

        self._repo.save(loan)
        self._events.dispatch(loan.pop_events())
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

**`domain_events.py`** — 인프로세스 어댑터
```python
from collections.abc import Callable


class InProcessDomainEventDispatcher:
    def __init__(self, handlers: tuple[Callable[[object], None], ...] = ()) -> None:
        self._handlers = handlers

    def dispatch(self, events: tuple[object, ...]) -> None:
        for event in events:
            for handler in self._handlers:
                handler(event)
```

**`core/dependencies.py`** — 조립 지점
```python
from app.application.services.lending.borrow_book_service import BorrowBookService
from app.infrastructure.domain_events import InProcessDomainEventDispatcher
from app.infrastructure.repositories.lending.in_memory_loan_repository import (
    InMemoryLoanRepository,
)

_service = BorrowBookService(
    InMemoryLoanRepository(),
    InProcessDomainEventDispatcher(),
)


def get_borrow_book_service() -> BorrowBookService:
    return _service
```

**`request.py`** — DTO (도메인 아님)
```python
from pydantic import BaseModel, ConfigDict, Field


class BorrowBookRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    member_id: str = Field(min_length=1, strict=True)
    book_id: str = Field(min_length=1, strict=True)


class LoanResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    loan_id: str
```

**`loan_router.py`**
```python
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.application.services.lending.borrow_book_service import (
    BorrowBookCommand, BorrowBookService,
)
from app.core.dependencies import get_borrow_book_service
from app.presentation.api.lending.request import BorrowBookRequest, LoanResponse

_router = APIRouter(prefix="/loans", tags=["loans"])


@_router.post("", response_model=LoanResponse, status_code=status.HTTP_201_CREATED)
def borrow_book(
    body: BorrowBookRequest,
    service: Annotated[BorrowBookService, Depends(get_borrow_book_service)],
) -> LoanResponse:
    try:
        loan_id = service.handle(
            BorrowBookCommand(member_id=body.member_id, book_id=body.book_id)
        )
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e
    return LoanResponse(loan_id=str(loan_id.value))

router = _router
```

---

다음: [06-test.ko.md](./06-test.ko.md)
