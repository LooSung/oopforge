from app.application.query.history_summary import HistorySummary
from app.domain.calculation.model import Calculation
from app.infrastructure.repositories.store import CalculationStore


class InMemoryCalculationRepository:
    """Write adapter: persists the aggregate and projects the read model."""

    def __init__(self, store: CalculationStore) -> None:
        self._store = store

    def save(self, calculation: Calculation) -> None:
        self._store.calculations[calculation.id] = calculation
        self._store.history.append(HistorySummary.from_calculation(calculation))
