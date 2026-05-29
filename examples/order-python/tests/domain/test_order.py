import pytest

from app.domain.order.model import Order, OrderPlaced, OrderStatus
from app.domain.order.value import CustomerId, OrderId, OrderLine


def test_place_creates_order_and_emits_event() -> None:
    order_id = OrderId.generate()
    customer_id = CustomerId("cust-1")
    lines = [OrderLine("p-1", 2, 1000)]

    order = Order.place(order_id, customer_id, lines)

    assert order.status is OrderStatus.PLACED
    assert order.total_amount() == 2000
    events = order.pop_events()
    assert len(events) == 1
    assert isinstance(events[0], OrderPlaced)
    assert events[0].total_amount == 2000


def test_place_rejects_empty_lines() -> None:
    with pytest.raises(ValueError, match="at least one line"):
        Order.place(OrderId.generate(), CustomerId("cust-1"), [])


def test_cancel_changes_status() -> None:
    order = Order.place(
        OrderId.generate(),
        CustomerId("cust-1"),
        [OrderLine("p-1", 1, 500)],
    )
    order.pop_events()
    order.cancel()
    assert order.status is OrderStatus.CANCELLED
