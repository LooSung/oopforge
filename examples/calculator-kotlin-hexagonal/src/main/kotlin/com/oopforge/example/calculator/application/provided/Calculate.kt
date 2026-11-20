package com.oopforge.example.calculator.application.provided

import com.oopforge.example.calculator.domain.Operator

interface Calculate {

    fun handle(command: CalculateCommand): CalculationResult

    data class CalculateCommand(val operandA: Double, val operator: Operator, val operandB: Double)

    data class CalculationResult(
        val calculationId: String,
        val operandA: Double,
        val operator: Operator,
        val operandB: Double,
        val result: Double,
    )
}
