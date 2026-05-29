from typing import Protocol

from app.domain.order.model import Order
from app.domain.order.value import OrderId


class OrderRepository(Protocol):
    def save(self, order: Order) -> None: ...

    def find_by_id(self, order_id: OrderId) -> Order | None: ...
