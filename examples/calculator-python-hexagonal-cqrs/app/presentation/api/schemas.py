from datetime import datetime
from typing import Annotated

from pydantic import AllowInfNan, BaseModel, ConfigDict, Field, Strict

from app.domain.calculation.model import Operator

StrictFiniteFloat = Annotated[float, Strict(), AllowInfNan(False)]


class CalculateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    operand_a: StrictFiniteFloat
    operand_b: StrictFiniteFloat
    operator: Operator


class CalculationCreatedResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    calculation_id: str


class HistoryEntryResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    calculation_id: str
    operand_a: float
    operand_b: float
    operator: str
    result: float
    performed_at: datetime


class HistoryListResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    items: list[HistoryEntryResponse] = Field(default_factory=list)
