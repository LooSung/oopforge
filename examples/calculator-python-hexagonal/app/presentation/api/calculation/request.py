from typing import Annotated

from pydantic import AllowInfNan, BaseModel, ConfigDict, Strict

from app.domain.calculation.model import Operator

StrictFiniteFloat = Annotated[float, Strict(), AllowInfNan(False)]


class CalculateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    operand_a: StrictFiniteFloat
    operator: Operator
    operand_b: StrictFiniteFloat

    def fingerprint(self) -> tuple[float, str, float]:
        return (float(self.operand_a), self.operator.value, float(self.operand_b))


class CalculationResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    calculation_id: str
    operand_a: float
    operator: str
    operand_b: float
    result: float
