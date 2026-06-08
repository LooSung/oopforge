from typing import Protocol

from app.domain.calculation.model import Calculation
from app.domain.calculation.value import CalculationId


class CalculationRepository(Protocol):
    def save(self, calculation: Calculation) -> None: ...

    def find_by_id(self, calculation_id: CalculationId) -> Calculation | None: ...
