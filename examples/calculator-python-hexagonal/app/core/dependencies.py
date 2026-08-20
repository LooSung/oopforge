from app.application.services.calculation.calculate_service import CalculateService
from app.infrastructure.repositories.calculation.in_memory_calculation_repository import (
    InMemoryCalculationRepository,
)

_repository = InMemoryCalculationRepository()
_service = CalculateService(_repository)


def get_calculate_service() -> CalculateService:
    return _service
