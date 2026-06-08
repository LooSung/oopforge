from typing import Protocol

from app.application.query.history_summary import HistorySummary
from app.domain.calculation.value import CalculationId


class HistoryQueryRepository(Protocol):
    """Read-side (query) port — returns read models, never aggregates."""

    def list_recent(self, limit: int) -> list[HistorySummary]: ...

    def find_by_id(self, calculation_id: CalculationId) -> HistorySummary | None: ...
