from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_order_service
from app.order.schemas import OrderResponse, PlaceOrderRequest
from app.order.service import OrderService

router = APIRouter(prefix="/api/v1/orders", tags=["Order"])


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def place_order(
    body: PlaceOrderRequest,
    service: OrderService = Depends(get_order_service),
) -> OrderResponse:
    order_id = service.place(body)
    return OrderResponse(order_id=str(order_id.value))
