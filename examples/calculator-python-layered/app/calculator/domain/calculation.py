from dataclasses import dataclass
from datetime import UTC, datetime
from enum import Enum
from uuid import UUID, uuid4


class Operator(str, Enum):
    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"

    def apply(self, a: float, b: float) -> float:
        if self is Operator.ADD:
            return a + b
        if self is Operator.SUBTRACT:
            return a - b
        if self is Operator.MULTIPLY:
            return a * b
        if b == 0:
            raise ValueError("division by zero")
        return a / b


@dataclass(frozen=True)
class CalculationId:
    value: UUID

    @staticmethod
    def generate() -> "CalculationId":
        return CalculationId(uuid4())

    @staticmethod
    def parse(raw: str) -> "CalculationId":
        return CalculationId(UUID(raw))


@dataclass(frozen=True)
class Calculation:
    id: CalculationId
    operand_a: float
    operator: Operator
    operand_b: float
    result: float
    performed_at: datetime

    @staticmethod
    def perform(
        calculation_id: CalculationId,
        operand_a: float,
        operator: Operator,
        operand_b: float,
    ) -> "Calculation":
        result = operator.apply(operand_a, operand_b)
        return Calculation._from_result(
            calculation_id, operand_a, operator, operand_b, result
        )

    @staticmethod
    def _from_result(
        calculation_id: CalculationId,
        operand_a: float,
        operator: Operator,
        operand_b: float,
        result: float,
    ) -> "Calculation":
        return Calculation(
            id=calculation_id,
            operand_a=operand_a,
            operator=operator,
            operand_b=operand_b,
            result=result,
            performed_at=datetime.now(UTC),
        )
