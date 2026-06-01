import pytest

from app.order.domain import CustomerId, Order, OrderId, OrderLine, OrderPlaced, OrderStatus


def test_place_creates_order_and_emits_event() -> None:
    order = Order.place(
        OrderId.generate(),
        CustomerId("cust-1"),
        [OrderLine("p-1", 2, 1000)],
    )
    assert order.status is OrderStatus.PLACED
    assert order.total_amount() == 2000
    events = order.pop_events()
    assert len(events) == 1
    assert isinstance(events[0], OrderPlaced)


def test_place_rejects_empty_lines() -> None:
    with pytest.raises(ValueError, match="at least one line"):
        Order.place(OrderId.generate(), CustomerId("cust-1"), [])
