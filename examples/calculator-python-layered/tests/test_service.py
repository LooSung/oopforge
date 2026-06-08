from app.calculator.domain.calculation import Operator
from app.calculator.repository.calculation_repository import CalculationRepository
from app.calculator.service.calculator_service import CalculatorService


def test_calculate_returns_result() -> None:
    service = CalculatorService(CalculationRepository())
    result = service.calculate(6, Operator.MULTIPLY, 7)
    assert result.result == 42
    assert result.calculation_id
