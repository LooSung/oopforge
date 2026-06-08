from dataclasses import dataclass, field

from app.application.query.history_summary import HistorySummary
from app.domain.calculation.model import Calculation
from app.domain.calculation.value import CalculationId


@dataclass
class CalculationStore:
    """Shared in-memory backing store: write model + read projection."""

    calculations: dict[CalculationId, Calculation] = field(default_factory=dict)
    history: list[HistorySummary] = field(default_factory=list)
