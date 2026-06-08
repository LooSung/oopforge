from app.calculator.repository.calculation_repository import CalculationRepository
from app.calculator.service.calculator_service import CalculatorService

_repository = CalculationRepository()
_service = CalculatorService(_repository)


def get_calculator_service() -> CalculatorService:
    return _service
