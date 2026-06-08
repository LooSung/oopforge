from typing import Protocol

from app.domain.calculation.model import Calculation


class CalculationRepository(Protocol):
    """Write-side (command) port — persists the aggregate."""

    def save(self, calculation: Calculation) -> None: ...
