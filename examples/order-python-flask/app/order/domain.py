from dataclasses import dataclass
from datetime import UTC, datetime
from enum import Enum
from uuid import UUID, uuid4


class OrderStatus(str, Enum):
    PLACED = "PLACED"
    CANCELLED = "CANCELLED"


@dataclass(frozen=True)
class OrderId:
    value: UUID

    @staticmethod
    def generate() -> "OrderId":
        return OrderId(uuid4())


@dataclass(frozen=True)
class CustomerId:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("customer id must not be blank")


@dataclass(frozen=True)
class OrderLine:
    product_id: str
    quantity: int
    unit_price: int

    def __post_init__(self) -> None:
        if not self.product_id.strip():
            raise ValueError("product id must not be blank")
        if self.quantity <= 0:
            raise ValueError("quantity must be positive")
        if self.unit_price < 0:
            raise ValueError("unit price must not be negative")

    def line_total(self) -> int:
        return self.quantity * self.unit_price


@dataclass(frozen=True)
class DomainEvent:
    event_id: str
    occurred_at: datetime


@dataclass(frozen=True)
class OrderPlaced(DomainEvent):
    order_id: OrderId
    customer_id: CustomerId
    total_amount: int


@dataclass
class Order:
    id: OrderId
    customer_id: CustomerId
    lines: tuple[OrderLine, ...]
    status: OrderStatus
    _events: list[DomainEvent]

    @staticmethod
    def place(order_id: OrderId, customer_id: CustomerId, lines: list[OrderLine]) -> "Order":
        if not lines:
            raise ValueError("order must have at least one line")
        frozen_lines = tuple(lines)
        order = Order(
            id=order_id,
            customer_id=customer_id,
            lines=frozen_lines,
            status=OrderStatus.PLACED,
            _events=[],
        )
        order._record(
            OrderPlaced(
                event_id=str(uuid4()),
                occurred_at=datetime.now(UTC),
                order_id=order_id,
                customer_id=customer_id,
                total_amount=order.total_amount(),
            )
        )
        return order

    def cancel(self) -> None:
        if self.status is OrderStatus.CANCELLED:
            raise ValueError("order is already cancelled")
        self.status = OrderStatus.CANCELLED

    def total_amount(self) -> int:
        return sum(line.line_total() for line in self.lines)

    def pop_events(self) -> list[DomainEvent]:
        published = list(self._events)
        self._events.clear()
        return published

    def _record(self, event: DomainEvent) -> None:
        self._events.append(event)
