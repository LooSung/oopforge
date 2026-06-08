from pydantic import BaseModel, Field

from app.domain.calculation.model import Operator


class CalculateRequest(BaseModel):
    operand_a: float
    operand_b: float
    operator: Operator


class CalculationCreatedResponse(BaseModel):
    calculation_id: str


class HistoryEntryResponse(BaseModel):
    calculation_id: str
    operand_a: float
    operand_b: float
    operator: str
    result: float
    performed_at: str


class HistoryListResponse(BaseModel):
    items: list[HistoryEntryResponse] = Field(default_factory=list)
