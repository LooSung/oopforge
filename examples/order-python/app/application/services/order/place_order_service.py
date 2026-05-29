from dataclasses import dataclass

from app.domain.order.model import Order
from app.domain.order.repository import OrderRepository
from app.domain.order.value import CustomerId, OrderId, OrderLine


@dataclass(frozen=True)
class PlaceOrderCommand:
    customer_id: str
    lines: list[tuple[str, int, int]]


class PlaceOrderService:
    def __init__(self, order_repository: OrderRepository) -> None:
        self._order_repository = order_repository

    def handle(self, command: PlaceOrderCommand) -> OrderId:
        order_id = OrderId.generate()
        customer_id = CustomerId(command.customer_id)
        lines = [
            OrderLine(product_id=product_id, quantity=quantity, unit_price=unit_price)
            for product_id, quantity, unit_price in command.lines
        ]
        order = Order.place(order_id, customer_id, lines)
        self._order_repository.save(order)
        order.pop_events()
        return order_id
