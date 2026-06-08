from dataclasses import dataclass

from app.domain.calculation.model import Calculation, Operator
from app.domain.calculation.repository import CalculationRepository
from app.domain.calculation.value import CalculationId


@dataclass(frozen=True)
class CalculateCommand:
    operand_a: float
    operator: Operator
    operand_b: float


@dataclass(frozen=True)
class CalculationResult:
    calculation_id: str
    operand_a: float
    operator: str
    operand_b: float
    result: float


class CalculateService:
    def __init__(self, calculation_repository: CalculationRepository) -> None:
        self._calculation_repository = calculation_repository

    def handle(self, command: CalculateCommand) -> CalculationResult:
        calculation = Calculation.perform(
            CalculationId.generate(),
            command.operand_a,
            command.operator,
            command.operand_b,
        )
        self._calculation_repository.save(calculation)
        calculation.pop_events()
        return CalculationResult(
            calculation_id=str(calculation.id.value),
            operand_a=calculation.operand_a,
            operator=calculation.operator.value,
            operand_b=calculation.operand_b,
            result=calculation.result,
        )
