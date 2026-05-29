from pydantic import BaseModel, Field


class LineRequest(BaseModel):
    product_id: str
    quantity: int = Field(gt=0)
    unit_price: int = Field(ge=0)


class PlaceOrderRequest(BaseModel):
    customer_id: str
    lines: list[LineRequest]


class OrderResponse(BaseModel):
    order_id: str
