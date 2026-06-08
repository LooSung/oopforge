from dataclasses import dataclass

from app.calculator.domain.calculation import Calculation, CalculationId, Operator
from app.calculator.repository.calculation_repository import CalculationRepository


@dataclass(frozen=True)
class CalculationResult:
    calculation_id: str
    operand_a: float
    operator: str
    operand_b: float
    result: float


class CalculatorService:
    def __init__(self, repository: CalculationRepository) -> None:
        self._repository = repository

    def calculate(self, operand_a: float, operator: Operator, operand_b: float) -> CalculationResult:
        calculation = Calculation.perform(CalculationId.generate(), operand_a, operator, operand_b)
        self._repository.save(calculation)
        calculation.pop_events()
        return CalculationResult(
            calculation_id=str(calculation.id.value),
            operand_a=calculation.operand_a,
            operator=calculation.operator.value,
            operand_b=calculation.operand_b,
            result=calculation.result,
        )
