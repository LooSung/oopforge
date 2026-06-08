from app.application.command.calculate_command_service import CalculateCommandService
from app.application.query.history_query_service import HistoryQueryService
from app.domain.calculation.model import Operator
from app.infrastructure.repositories.in_memory_calculation_repository import (
    InMemoryCalculationRepository,
)
from app.infrastructure.repositories.in_memory_history_query_repository import (
    InMemoryHistoryQueryRepository,
)
from app.infrastructure.repositories.store import CalculationStore


def test_query_lists_history_after_command() -> None:
    store = CalculationStore()
    command = CalculateCommandService(InMemoryCalculationRepository(store))
    query = HistoryQueryService(InMemoryHistoryQueryRepository(store))

    command.calculate(1, Operator.ADD, 2)
    command.calculate(5, Operator.MULTIPLY, 3)

    history = query.list_recent(limit=10)
    assert len(history) == 2
    assert history[0].result == 15
    assert history[1].result == 3
