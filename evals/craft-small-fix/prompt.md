---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Use OOPforge craft: members can borrow at most 3 books, but the check lets a 4th loan through. Fix it. This session cannot edit files, so reply with the change.

`app/domain/loan/member.py`:

```python
class LoanLimitExceeded(Exception):
    pass


class Member:
    MAX_ACTIVE_LOANS = 3

    def __init__(self, member_id: str, active_loans: int = 0) -> None:
        self.member_id = member_id
        self.active_loans = active_loans

    def borrow(self) -> None:
        if self.active_loans > self.MAX_ACTIVE_LOANS:
            raise LoanLimitExceeded(self.member_id)
        self.active_loans += 1
```
