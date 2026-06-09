# Step 5 — Test

[English](./05-test.md) · [한국어](./05-test.ko.md)
Domain 테스트는 Spring·DB fixture **없이** 실행. 유스케이스 테스트는 in-memory port 사용.

---

## Java (JUnit 5)

### Domain — Spring context 불필요

```java
package com.example.lending.domain;

import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.*;

class LoanTest {

    @Test
    void borrow_sets_active_status() {
        Loan loan = Loan.borrow(LoanId.generate(), new MemberId("m-1"), new BookId("b-1"));
        assertThat(loan.status()).isEqualTo(LoanStatus.ACTIVE);
    }

    @Test
    void borrow_emits_book_borrowed_event() {
        Loan loan = Loan.borrow(LoanId.generate(), new MemberId("m-1"), new BookId("b-1"));
        assertThat(loan.popEvents()).hasSize(1).first().isInstanceOf(BookBorrowed.class);
    }

    @Test
    void return_twice_throws() {
        Loan loan = Loan.borrow(LoanId.generate(), new MemberId("m-1"), new BookId("b-1"));
        loan.returnBook();
        assertThatThrownBy(loan::returnBook).isInstanceOf(IllegalStateException.class);
    }
}
```

---

## Java — 유스케이스

```java
package com.example.lending.application.service;

import com.example.lending.adapter.persistence.InMemoryLoanRepository;
import com.example.lending.application.provided.BorrowBook;
import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.*;

class BorrowBookServiceTest {

    @Test
    void borrow_returns_loan_id() {
        var service = new BorrowBookService(new InMemoryLoanRepository());
        String loanId = service.handle(new BorrowBook.Command("member-1", "book-1"));
        assertThat(loanId).isNotBlank();
    }

    @Test
    void cannot_borrow_same_book_twice() {
        var service = new BorrowBookService(new InMemoryLoanRepository());
        service.handle(new BorrowBook.Command("member-1", "book-1"));
        assertThatThrownBy(() ->
            service.handle(new BorrowBook.Command("member-2", "book-1"))
        ).isInstanceOf(IllegalStateException.class)
         .hasMessageContaining("book already on loan");
    }
}
```

---

## Python (pytest)

### Domain

```python
import pytest

from app.domain.lending.model import Loan, LoanStatus, BookBorrowed
from app.domain.lending.value import BookId, LoanId, MemberId
from app.application.services.lending.borrow_book_service import (
    BorrowBookCommand, BorrowBookService,
)
from app.infrastructure.repositories.lending.in_memory_loan_repository import (
    InMemoryLoanRepository,
)


def test_borrow_sets_active():
    loan = Loan.borrow(LoanId.generate(), MemberId("m-1"), BookId("b-1"))
    assert loan.status is LoanStatus.ACTIVE


def test_borrow_emits_event():
    loan = Loan.borrow(LoanId.generate(), MemberId("m-1"), BookId("b-1"))
    events = loan.pop_events()
    assert len(events) == 1
    assert isinstance(events[0], BookBorrowed)


def test_return_twice_raises():
    loan = Loan.borrow(LoanId.generate(), MemberId("m-1"), BookId("b-1"))
    loan.return_book()
    with pytest.raises(ValueError, match="loan already returned"):
        loan.return_book()


def test_use_case_borrow_success():
    service = BorrowBookService(InMemoryLoanRepository())
    loan_id = service.handle(BorrowBookCommand("member-1", "book-1"))
    assert loan_id is not None


def test_use_case_duplicate_borrow_fails():
    service = BorrowBookService(InMemoryLoanRepository())
    service.handle(BorrowBookCommand("member-1", "book-1"))
    with pytest.raises(ValueError, match="book already on loan"):
        service.handle(BorrowBookCommand("member-2", "book-1"))
```

---

다음: [06-layer-rules.ko.md](./06-layer-rules.ko.md)
