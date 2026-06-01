from pydantic import BaseModel, Field


class OrderLineRequest(BaseModel):
    product_id: str
    quantity: int = Field(ge=1)
    unit_price: int = Field(ge=0)


class PlaceOrderRequest(BaseModel):
    customer_id: str
    lines: list[OrderLineRequest] = Field(min_length=1)


class OrderResponse(BaseModel):
    order_id: str
