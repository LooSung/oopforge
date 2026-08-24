from dataclasses import FrozenInstanceError

import pytest

from app.domain.calculation.model import Calculation, CalculationPerformed, Operator
from app.domain.calculation.value import CalculationId


def test_perform_computes_result_and_emits_event() -> None:
    calculation_id = CalculationId.generate()
    calculation = Calculation.perform(calculation_id, 2, Operator.ADD, 3)

    assert calculation.result == 5
    events = calculation.pop_events()
    assert len(events) == 1
    assert isinstance(events[0], CalculationPerformed)
    assert events[0].calculation_id == calculation_id
    assert events[0].result == 5
    assert events[0].occurred_at == calculation.performed_at
    assert calculation.pop_events() == []


def test_calculation_state_is_read_only() -> None:
    calculation = Calculation.perform(CalculationId.generate(), 2, Operator.ADD, 3)

    with pytest.raises(FrozenInstanceError):
        setattr(calculation, "result", 99)


def test_division_by_zero_raises() -> None:
    with pytest.raises(ValueError, match="division by zero"):
        Calculation.perform(CalculationId.generate(), 1, Operator.DIVIDE, 0)
