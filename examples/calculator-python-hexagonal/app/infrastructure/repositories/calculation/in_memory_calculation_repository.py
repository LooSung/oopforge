from app.domain.calculation.model import Calculation
from app.domain.calculation.value import CalculationId


class InMemoryCalculationRepository:
    def __init__(self) -> None:
        self._store: dict[CalculationId, Calculation] = {}

    def save(self, calculation: Calculation) -> None:
        self._store[calculation.id] = calculation

    def find_by_id(self, calculation_id: CalculationId) -> Calculation | None:
        return self._store.get(calculation_id)
