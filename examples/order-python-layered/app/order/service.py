from app.order.domain import CustomerId, Order, OrderId, OrderLine
from app.order.repository import OrderRepository
from app.order.schemas import PlaceOrderRequest


class OrderService:
    def __init__(self, repository: OrderRepository) -> None:
        self._repository = repository

    def place(self, request: PlaceOrderRequest) -> OrderId:
        order_id = OrderId.generate()
        customer_id = CustomerId(request.customer_id)
        lines = [
            OrderLine(
                product_id=line.product_id,
                quantity=line.quantity,
                unit_price=line.unit_price,
            )
            for line in request.lines
        ]
        order = Order.place(order_id, customer_id, lines)
        self._repository.save(order)
        order.pop_events()
        return order_id
