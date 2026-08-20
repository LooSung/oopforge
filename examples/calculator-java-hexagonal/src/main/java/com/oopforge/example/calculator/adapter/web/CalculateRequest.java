package com.oopforge.example.calculator.adapter.web;

import com.oopforge.example.calculator.domain.Operator;
import jakarta.validation.constraints.AssertTrue;
import jakarta.validation.constraints.NotNull;

public record CalculateRequest(
        @NotNull Double operandA,
        @NotNull Operator operator,
        @NotNull Double operandB) {

    @AssertTrue(message = "operands must be finite")
    public boolean hasFiniteOperands() {
        return isFinite(operandA) && isFinite(operandB);
    }

    private boolean isFinite(Double value) {
        return value == null || Double.isFinite(value);
    }
}
