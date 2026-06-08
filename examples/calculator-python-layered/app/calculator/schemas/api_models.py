from pydantic import BaseModel

from app.calculator.domain.calculation import Operator


class CalculateRequest(BaseModel):
    operand_a: float
    operator: Operator
    operand_b: float


class CalculationResponse(BaseModel):
    calculation_id: str
    operand_a: float
    operator: str
    operand_b: float
    result: float
