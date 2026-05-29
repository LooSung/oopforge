from app.application.services.order.place_order_service import PlaceOrderCommand, PlaceOrderService
from app.infrastructure.repositories.order.in_memory_order_repository import InMemoryOrderRepository


def test_handle_persists_order() -> None:
    service = PlaceOrderService(InMemoryOrderRepository())
    order_id = service.handle(
        PlaceOrderCommand(customer_id="cust-1", lines=[("p-1", 1, 900)])
    )
    assert order_id.value is not None
