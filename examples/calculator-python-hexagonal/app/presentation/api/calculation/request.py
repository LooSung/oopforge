from pydantic import BaseModel, ConfigDict, FiniteFloat

from app.domain.calculation.model import Operator


class CalculateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    operand_a: FiniteFloat
    operator: Operator
    operand_b: FiniteFloat

    def fingerprint(self) -> tuple[float, str, float]:
        return (float(self.operand_a), self.operator.value, float(self.operand_b))


class CalculationResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    calculation_id: str
    operand_a: float
    operator: str
    operand_b: float
    result: float
