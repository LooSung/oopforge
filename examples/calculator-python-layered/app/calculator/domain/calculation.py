from dataclasses import dataclass, field
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
class DomainEvent:
    event_id: str
    occurred_at: datetime


@dataclass(frozen=True)
class CalculationPerformed(DomainEvent):
    calculation_id: CalculationId
    result: float


@dataclass
class Calculation:
    id: CalculationId
    operand_a: float
    operator: Operator
    operand_b: float
    result: float
    performed_at: datetime
    _events: list[DomainEvent] = field(default_factory=list)

    @staticmethod
    def perform(
        calculation_id: CalculationId,
        operand_a: float,
        operator: Operator,
        operand_b: float,
    ) -> "Calculation":
        result = operator.apply(operand_a, operand_b)
        calculation = Calculation(
            id=calculation_id,
            operand_a=operand_a,
            operator=operator,
            operand_b=operand_b,
            result=result,
            performed_at=datetime.now(UTC),
        )
        calculation._record(
            CalculationPerformed(
                event_id=str(uuid4()),
                occurred_at=calculation.performed_at,
                calculation_id=calculation_id,
                result=result,
            )
        )
        return calculation

    def pop_events(self) -> list[DomainEvent]:
        published = list(self._events)
        self._events.clear()
        return published

    def _record(self, event: DomainEvent) -> None:
        self._events.append(event)
