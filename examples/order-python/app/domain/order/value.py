from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass(frozen=True)
class OrderId:
    value: UUID

    @staticmethod
    def generate() -> "OrderId":
        return OrderId(uuid4())


@dataclass(frozen=True)
class CustomerId:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("customer id must not be blank")


@dataclass(frozen=True)
class OrderLine:
    product_id: str
    quantity: int
    unit_price: int

    def __post_init__(self) -> None:
        if not self.product_id.strip():
            raise ValueError("product id must not be blank")
        if self.quantity <= 0:
            raise ValueError("quantity must be positive")
        if self.unit_price < 0:
            raise ValueError("unit price must not be negative")

    def line_total(self) -> int:
        return self.quantity * self.unit_price
