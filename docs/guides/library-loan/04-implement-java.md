# Step 4 — Implement (Java)

[English](./04-implement-java.md) · [한국어](./04-implement-java.ko.md)
Domain → application → adapter order. **Domain layer: Spring import 0.**

---

## Domain

**`LoanId.java`**
```java
package com.example.lending.domain;

import java.util.UUID;

public record LoanId(UUID value) {
    public static LoanId generate() {
        return new LoanId(UUID.randomUUID());
    }
}
```

**`MemberId.java`**
```java
package com.example.lending.domain;

public record MemberId(String value) {
    public MemberId {
        if (value == null || value.isBlank()) {
            throw new IllegalArgumentException("member id must not be blank");
        }
    }
}
```

**`BookId.java`**
```java
package com.example.lending.domain;

public record BookId(String value) {
    public BookId {
        if (value == null || value.isBlank()) {
            throw new IllegalArgumentException("book id must not be blank");
        }
    }
}
```

**`LoanStatus.java`**
```java
package com.example.lending.domain;

public enum LoanStatus {
    ACTIVE, RETURNED
}
```

**`BookBorrowed.java`**
```java
package com.example.lending.domain;

import java.time.Instant;

public record BookBorrowed(
    LoanId loanId,
    MemberId memberId,
    BookId bookId,
    Instant borrowedAt
) {}
```

**`Loan.java`** — Aggregate Root
```java
package com.example.lending.domain;

import java.time.Instant;
import java.util.ArrayList;
import java.util.List;

public class Loan {

    private final LoanId id;
    private final MemberId memberId;
    private final BookId bookId;
    private final Instant borrowedAt;
    private LoanStatus status;
    private final List<Object> domainEvents = new ArrayList<>();

    private Loan(LoanId id, MemberId memberId, BookId bookId, Instant borrowedAt) {
        this.id = id;
        this.memberId = memberId;
        this.bookId = bookId;
        this.borrowedAt = borrowedAt;
        this.status = LoanStatus.ACTIVE;
    }

    public static Loan borrow(LoanId id, MemberId memberId, BookId bookId) {
        Loan loan = new Loan(id, memberId, bookId, Instant.now());
        loan.record(new BookBorrowed(id, memberId, bookId, loan.borrowedAt));
        return loan;
    }

    public void returnBook() {
        if (this.status == LoanStatus.RETURNED) {
            throw new IllegalStateException("loan already returned");
        }
        this.status = LoanStatus.RETURNED;
    }

    public List<Object> popEvents() {
        List<Object> published = List.copyOf(domainEvents);
        domainEvents.clear();
        return published;
    }

    public LoanId id() { return id; }
    public BookId bookId() { return bookId; }
    public LoanStatus status() { return status; }

    private void record(Object event) {
        domainEvents.add(event);
    }
}
```

---

## Application

**`BorrowBook.java`** — inbound port
```java
package com.example.lending.application.provided;

public interface BorrowBook {
    record Command(String memberId, String bookId) {}
    String handle(Command command);
}
```

**`LoanRepository.java`** — outbound port
```java
package com.example.lending.application.required;

import com.example.lending.domain.*;
import java.util.Optional;

public interface LoanRepository {
    Optional<Loan> findById(LoanId id);
    Optional<Loan> findActiveLoanByBookId(BookId bookId);
    void save(Loan loan);
}
```

**`BorrowBookService.java`**
```java
package com.example.lending.application.service;

import com.example.lending.application.provided.BorrowBook;
import com.example.lending.application.required.LoanRepository;
import com.example.lending.domain.*;

public class BorrowBookService implements BorrowBook {

    private final LoanRepository loanRepository;

    public BorrowBookService(LoanRepository loanRepository) {
        this.loanRepository = loanRepository;
    }

    @Override
    public String handle(Command command) {
        BookId bookId = new BookId(command.bookId());

        loanRepository.findActiveLoanByBookId(bookId).ifPresent(existing -> {
            throw new IllegalStateException("book already on loan: " + bookId.value());
        });

        LoanId loanId = LoanId.generate();
        MemberId memberId = new MemberId(command.memberId());
        Loan loan = Loan.borrow(loanId, memberId, bookId);

        loanRepository.save(loan);
        loan.popEvents();

        return loanId.value().toString();
    }
}
```

---

## Adapter

**`InMemoryLoanRepository.java`**
```java
package com.example.lending.adapter.persistence;

import com.example.lending.application.required.LoanRepository;
import com.example.lending.domain.*;
import java.util.*;

public class InMemoryLoanRepository implements LoanRepository {

    private final Map<LoanId, Loan> store = new HashMap<>();

    @Override
    public Optional<Loan> findById(LoanId id) {
        return Optional.ofNullable(store.get(id));
    }

    @Override
    public Optional<Loan> findActiveLoanByBookId(BookId bookId) {
        return store.values().stream()
            .filter(l -> l.bookId().equals(bookId) && l.status() == LoanStatus.ACTIVE)
            .findFirst();
    }

    @Override
    public void save(Loan loan) {
        store.put(loan.id(), loan);
    }
}
```

**`LoanController.java`**
```java
package com.example.lending.adapter.web;

import com.example.lending.application.provided.BorrowBook;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/loans")
public class LoanController {

    private final BorrowBook borrowBook;

    public LoanController(BorrowBook borrowBook) {
        this.borrowBook = borrowBook;
    }

    @PostMapping
    public ResponseEntity<LoanResponse> borrow(@RequestBody BorrowBookRequest request) {
        String loanId = borrowBook.handle(
            new BorrowBook.Command(request.memberId(), request.bookId())
        );
        return ResponseEntity.status(201).body(new LoanResponse(loanId));
    }
}
```

---

Next: [05-test.md](./05-test.md) · Python: [04-implement-python.md](./04-implement-python.md)
