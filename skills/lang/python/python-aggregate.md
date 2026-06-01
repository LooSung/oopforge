---
name: python-aggregate
description: Python에서 Aggregate Root를 dataclass/Pydantic으로 안전하게 구현하는 패턴.
tags: [python, ddd, aggregate]
stability: stable
---

# Python — Aggregate Root

## 언제 쓰나
DDD Aggregate Root를 Python으로 구현할 때. `skills/oop/aggregate-root.md`의 언어 무관 규칙을 먼저 읽고 이 스킬로 구체화한다.

## 기준
Python에서 Aggregate는 다음 셋 중 하나로 구현한다.

| 구현 | 언제 |
|---|---|
| `@dataclass(frozen=False)` + 명시적 메서드 | 기본 권장. 가장 단순. |
| Pydantic v2 `BaseModel` | 검증을 모델 안에서 강제하고 싶을 때 |
| 일반 class | 동작이 복잡하고 dataclass 한계가 보일 때 |

**ORM 모델과 Aggregate는 분리한다.** 같은 클래스에 SQLAlchemy 어노테이션을 붙이면 도메인 무결성이 깨진다.

## 체크리스트
- [ ] Aggregate Root는 외부에서 `__init__` 직접 호출 금지 → `classmethod` 팩토리 (`Order.create(...)`)
- [ ] 모든 상태 변경은 의도된 메서드 (`order.place()`, `order.cancel()`) — setter/속성 직접 대입 금지
- [ ] 다른 Aggregate는 ID로만 참조 (`customer_id: CustomerId`, 객체 X)
- [ ] 컬렉션 노출 시 `tuple()` 또는 복사본 반환 (방어적 복사)
- [ ] 불변량(invariant)은 생성/변경 메서드에서 검증, 위반 시 도메인 예외
- [ ] 도메인 이벤트가 있으면 내부 리스트에 append, 외부에서 `pull_events()`로 회수
- [ ] FastAPI/SQLAlchemy/Flask import 0

## 템플릿 — dataclass 버전

```python
# domain/order/model.py
from dataclasses import dataclass, field
from typing import Iterable
from .value import OrderId, OrderLine, OrderStatus, CustomerId
from .event import OrderPlaced
from .exceptions import OrderInvariantError

@dataclass
class Order:
    id: OrderId
    customer_id: CustomerId
    _lines: list[OrderLine] = field(default_factory=list)
    status: OrderStatus = OrderStatus.DRAFT
    _events: list = field(default_factory=list, repr=False)

    # 외부 호출 금지: 항상 create() 통해 생성
    @classmethod
    def create(cls, id: OrderId, customer_id: CustomerId, lines: Iterable[OrderLine]) -> "Order":
        lines_list = list(lines)
        if not lines_list:
            raise OrderInvariantError("Order requires at least one line")
        order = cls(id=id, customer_id=customer_id, _lines=lines_list)
        order._events.append(OrderPlaced(order_id=id, customer_id=customer_id))
        return order

    @property
    def lines(self) -> tuple[OrderLine, ...]:
        return tuple(self._lines)  # 방어적 복사

    @property
    def total(self) -> int:
        return sum(line.amount for line in self._lines)

    def cancel(self, reason: str) -> None:
        if self.status in (OrderStatus.SHIPPED, OrderStatus.CANCELLED):
            raise OrderInvariantError(f"Cannot cancel order in status {self.status}")
        self.status = OrderStatus.CANCELLED

    def pull_events(self) -> list:
        events, self._events = self._events, []
        return events
```

## 템플릿 — Pydantic v2 버전

```python
# domain/order/model.py
from pydantic import BaseModel, Field, PrivateAttr
from .value import OrderId, OrderLine, OrderStatus, CustomerId

class Order(BaseModel):
    model_config = {"frozen": False, "arbitrary_types_allowed": True}

    id: OrderId
    customer_id: CustomerId
    status: OrderStatus = OrderStatus.DRAFT
    _lines: list[OrderLine] = PrivateAttr(default_factory=list)
    _events: list = PrivateAttr(default_factory=list)

    @classmethod
    def create(cls, id: OrderId, customer_id: CustomerId, lines: list[OrderLine]) -> "Order":
        if not lines:
            raise ValueError("Order requires at least one line")
        order = cls(id=id, customer_id=customer_id)
        order._lines = list(lines)
        return order

    @property
    def lines(self) -> tuple[OrderLine, ...]:
        return tuple(self._lines)
```

## ORM 매핑 분리

```python
# infrastructure/persistence/order_orm.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase): ...

class OrderOrm(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False)
    # ...

def to_domain(orm: OrderOrm) -> "Order": ...
def to_orm(domain: "Order") -> OrderOrm: ...
```

도메인 모델과 ORM 모델은 다른 파일·다른 클래스. Repository 어댑터가 양방향 변환을 담당.

## 금지
- **public setter** — 속성 직접 대입 금지. 의도된 메서드만.
- **다른 Aggregate를 객체로 참조** — 항상 ID. (`order.customer: Customer` 금지, `order.customer_id` OK)
- **컬렉션 그대로 노출** — `return self._lines` 금지. `tuple(self._lines)` 또는 새 list.
- **`__init__`을 외부에서 직접 호출** — 항상 `create()` 팩토리.
- **도메인 클래스에 `@Entity`/`Base`/`db.Model` 상속** — ORM과 분리.
- **유효성 검증을 생성자 외부로 미루기** — 생성/변경 시점에 즉시 검증, 실패 시 도메인 예외.

## 참고
- 작은 프로젝트에서는 ORM 모델이 곧 도메인 모델이 되는 단순화도 허용 (`fastapi-layered-layout.md` 참조). 그 경우에도 위 메서드 규칙은 유지.
- 이벤트 발행 패턴은 `python-domain-event.md` 참조.
