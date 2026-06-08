import pytest

from app.domain.calculation.model import Calculation, CalculationPerformed, Operator
from app.domain.calculation.value import CalculationId


def test_perform_computes_result_and_emits_event() -> None:
    calculation = Calculation.perform(CalculationId.generate(), 2, Operator.ADD, 3)

    assert calculation.result == 5
    events = calculation.pop_events()
    assert len(events) == 1
    assert isinstance(events[0], CalculationPerformed)
    assert events[0].result == 5


def test_division_by_zero_raises() -> None:
    with pytest.raises(ValueError, match="division by zero"):
        Calculation.perform(CalculationId.generate(), 1, Operator.DIVIDE, 0)
