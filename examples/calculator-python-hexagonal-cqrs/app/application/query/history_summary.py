from dataclasses import dataclass
from datetime import datetime

from app.domain.calculation.model import Calculation


@dataclass(frozen=True)
class HistorySummary:
    """Read model — denormalized projection for the query side, not a domain object."""

    calculation_id: str
    operand_a: float
    operand_b: float
    operator: str
    result: float
    performed_at: datetime

    @staticmethod
    def from_calculation(calculation: Calculation) -> "HistorySummary":
        return HistorySummary(
            calculation_id=str(calculation.id.value),
            operand_a=calculation.operand_a,
            operand_b=calculation.operand_b,
            operator=calculation.operator.value,
            result=calculation.result,
            performed_at=calculation.performed_at,
        )
