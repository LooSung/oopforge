package com.oopforge.example.calculator.adapter.web

import com.oopforge.example.calculator.domain.Operator
import jakarta.validation.constraints.AssertTrue
import jakarta.validation.constraints.NotNull

data class CalculateRequest(
    @field:NotNull val operandA: Double?,
    @field:NotNull val operator: Operator?,
    @field:NotNull val operandB: Double?,
) {

    @AssertTrue(message = "operands must be finite")
    fun hasFiniteOperands(): Boolean = TODO("Implement stage")
}
