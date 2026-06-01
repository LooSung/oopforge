from app.order.repository import OrderRepository
from app.order.service import OrderService

_repository = OrderRepository()
_service = OrderService(_repository)


def get_order_service() -> OrderService:
    return _service
