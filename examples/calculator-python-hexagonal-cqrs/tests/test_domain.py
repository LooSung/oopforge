import pytest

from app.domain.calculation.model import Calculation, CalculationPerformed, Operator
from app.domain.calculation.value import CalculationId


def test_addition_emits_event() -> None:
    calc = Calculation.perform(CalculationId.generate(), 2, Operator.ADD, 3)
    assert calc.result == 5
    events = calc.pop_events()
    assert len(events) == 1
    assert isinstance(events[0], CalculationPerformed)


def test_division_by_zero_raises() -> None:
    with pytest.raises(ValueError, match="division by zero"):
        Calculation.perform(CalculationId.generate(), 1, Operator.DIVIDE, 0)
