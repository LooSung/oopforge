from app.application.command.calculate_command_service import CalculateCommandService
from app.application.query.history_query_service import HistoryQueryService
from app.infrastructure.repositories.in_memory_calculation_repository import (
    InMemoryCalculationRepository,
)
from app.infrastructure.repositories.in_memory_history_query_repository import (
    InMemoryHistoryQueryRepository,
)
from app.infrastructure.repositories.store import CalculationStore

_store = CalculationStore()
_command_service = CalculateCommandService(InMemoryCalculationRepository(_store))
_query_service = HistoryQueryService(InMemoryHistoryQueryRepository(_store))


def get_command_service() -> CalculateCommandService:
    return _command_service


def get_query_service() -> HistoryQueryService:
    return _query_service
