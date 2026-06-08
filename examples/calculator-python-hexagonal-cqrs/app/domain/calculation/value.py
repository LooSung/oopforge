from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass(frozen=True)
class CalculationId:
    value: UUID

    @staticmethod
    def generate() -> "CalculationId":
        return CalculationId(uuid4())

    @staticmethod
    def parse(raw: str) -> "CalculationId":
        return CalculationId(UUID(raw))
