package com.oopforge.example.calculator.domain

import java.time.Instant

class Calculation private constructor(
    val id: CalculationId,
    val operandA: Double,
    val operator: Operator,
    val operandB: Double,
    val result: Double,
    val performedAt: Instant,
) {
    companion object {
        fun perform(id: CalculationId, operandA: Double, operator: Operator, operandB: Double): Calculation =
            TODO("Implement stage")
    }
}
