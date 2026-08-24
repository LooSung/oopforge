from dataclasses import FrozenInstanceError

import pytest

from app.calculator.domain.calculation import (
    Calculation,
    CalculationId,
    Operator,
)


def test_perform_computes_result() -> None:
    calculation = Calculation.perform(CalculationId.generate(), 2, Operator.ADD, 3)

    assert calculation.result == 5


def test_calculation_state_is_read_only() -> None:
    calculation = Calculation.perform(CalculationId.generate(), 2, Operator.ADD, 3)

    with pytest.raises(FrozenInstanceError):
        setattr(calculation, "result", 99)


def test_division_by_zero_raises() -> None:
    with pytest.raises(ValueError, match="division by zero"):
        Calculation.perform(CalculationId.generate(), 1, Operator.DIVIDE, 0)
