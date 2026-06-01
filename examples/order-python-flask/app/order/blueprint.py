from flask.views import MethodView
from flask_smorest import Blueprint

from app.core.dependencies import get_order_service
from app.order.schemas import OrderResponseSchema, PlaceOrderSchema

bp = Blueprint(
    "order",
    __name__,
    url_prefix="/api/v1/orders",
    description="Order placement (Flask 3-tier)",
)


@bp.route("")
class OrderCollection(MethodView):
    @bp.arguments(PlaceOrderSchema)
    @bp.response(201, OrderResponseSchema)
    def post(self, payload: dict) -> dict:
        order_id = get_order_service().place(payload)
        return {"order_id": str(order_id.value)}
