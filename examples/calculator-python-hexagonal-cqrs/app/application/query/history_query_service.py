from app.application.query.history_query_repository import HistoryQueryRepository
from app.application.query.history_summary import HistorySummary
from app.domain.calculation.value import CalculationId


class HistoryQueryService:
    """Read side: only reads projections — no state changes."""

    def __init__(self, query_repository: HistoryQueryRepository) -> None:
        self._query_repository = query_repository

    def list_recent(self, limit: int = 20) -> list[HistorySummary]:
        return self._query_repository.list_recent(limit)

    def get_by_id(self, calculation_id: CalculationId) -> HistorySummary | None:
        return self._query_repository.find_by_id(calculation_id)
