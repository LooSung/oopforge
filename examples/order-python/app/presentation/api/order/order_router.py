from fastapi import APIRouter, Depends, status

from app.application.services.order.place_order_service import PlaceOrderCommand, PlaceOrderService
from app.infrastructure.repositories.order.in_memory_order_repository import InMemoryOrderRepository
from app.presentation.api.order.request import OrderResponse, PlaceOrderRequest

_router = APIRouter(prefix="/orders", tags=["orders"])
_repository = InMemoryOrderRepository()
_service = PlaceOrderService(_repository)


def get_place_order_service() -> PlaceOrderService:
    return _service


@_router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def place_order(
    body: PlaceOrderRequest,
    service: PlaceOrderService = Depends(get_place_order_service),
) -> OrderResponse:
    command = PlaceOrderCommand(
        customer_id=body.customer_id,
        lines=[(line.product_id, line.quantity, line.unit_price) for line in body.lines],
    )
    order_id = service.handle(command)
    return OrderResponse(order_id=str(order_id.value))

router = _router
