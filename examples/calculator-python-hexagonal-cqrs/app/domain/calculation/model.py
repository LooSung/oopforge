from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from uuid import uuid4

from app.domain.calculation.value import CalculationId


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
class DomainEvent:
    event_id: str
    occurred_at: datetime


@dataclass(frozen=True)
class CalculationPerformed(DomainEvent):
    calculation_id: CalculationId
    result: float


@dataclass(frozen=True)
class Calculation:
    id: CalculationId
    operand_a: float
    operator: Operator
    operand_b: float
    result: float
    performed_at: datetime
    _events: tuple[DomainEvent, ...] = field(
        default_factory=tuple,
        init=False,
        repr=False,
        compare=False,
    )

    @staticmethod
    def perform(
        calculation_id: CalculationId,
        operand_a: float,
        operator: Operator,
        operand_b: float,
    ) -> "Calculation":
        result = operator.apply(operand_a, operand_b)
        calculation = Calculation._from_result(
            calculation_id, operand_a, operator, operand_b, result
        )
        calculation._record(calculation._performed_event())
        return calculation

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

    def _performed_event(self) -> CalculationPerformed:
        return CalculationPerformed(
            event_id=str(uuid4()),
            occurred_at=self.performed_at,
            calculation_id=self.id,
            result=self.result,
        )

    def pop_events(self) -> list[DomainEvent]:
        published = list(self._events)
        object.__setattr__(self, "_events", ())
        return published

    def _record(self, event: DomainEvent) -> None:
        object.__setattr__(self, "_events", (*self._events, event))
