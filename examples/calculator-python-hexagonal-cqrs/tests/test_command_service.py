from app.application.command.calculate_command_service import CalculateCommandService
from app.domain.calculation.model import Operator
from app.infrastructure.repositories.in_memory_calculation_repository import (
    InMemoryCalculationRepository,
)
from app.infrastructure.repositories.store import CalculationStore


def test_command_returns_id_not_history() -> None:
    service = CalculateCommandService(InMemoryCalculationRepository(CalculationStore()))
    calculation_id = service.calculate(10, Operator.ADD, 5)
    assert str(calculation_id.value)
