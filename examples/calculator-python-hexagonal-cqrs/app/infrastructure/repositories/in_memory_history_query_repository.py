from app.application.query.history_summary import HistorySummary
from app.domain.calculation.value import CalculationId
from app.infrastructure.repositories.store import CalculationStore


class InMemoryHistoryQueryRepository:
    """Read adapter: serves projections from the store."""

    def __init__(self, store: CalculationStore) -> None:
        self._store = store

    def list_recent(self, limit: int) -> list[HistorySummary]:
        if limit <= 0:
            raise ValueError("limit must be positive")
        return list(reversed(self._store.history[-limit:]))

    def find_by_id(self, calculation_id: CalculationId) -> HistorySummary | None:
        for entry in reversed(self._store.history):
            if entry.calculation_id == str(calculation_id.value):
                return entry
        return None
