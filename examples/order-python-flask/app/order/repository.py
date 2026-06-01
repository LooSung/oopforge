from app.order.domain import Order, OrderId


class OrderRepository:
    def __init__(self) -> None:
        self._store: dict[OrderId, Order] = {}

    def save(self, order: Order) -> None:
        self._store[order.id] = order

    def find_by_id(self, order_id: OrderId) -> Order | None:
        return self._store.get(order_id)
