from app.order.repository import OrderRepository
from app.order.service import OrderService


def test_place_returns_order_id() -> None:
    service = OrderService(OrderRepository())
    order_id = service.place(
        {
            "customer_id": "cust-1",
            "lines": [{"product_id": "p-1", "quantity": 2, "unit_price": 1000}],
        }
    )
    assert order_id is not None
