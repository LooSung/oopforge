from app.domain.calculation.model import Calculation, Operator
from app.domain.calculation.repository import CalculationRepository
from app.domain.calculation.value import CalculationId


class CalculateCommandService:
    """Write side: performs a calculation and returns only its ID."""

    def __init__(self, calculation_repository: CalculationRepository) -> None:
        self._calculation_repository = calculation_repository

    def calculate(self, operand_a: float, operator: Operator, operand_b: float) -> CalculationId:
        calculation_id = CalculationId.generate()
        calculation = Calculation.perform(calculation_id, operand_a, operator, operand_b)
        self._calculation_repository.save(calculation)
        calculation.pop_events()
        return calculation_id
