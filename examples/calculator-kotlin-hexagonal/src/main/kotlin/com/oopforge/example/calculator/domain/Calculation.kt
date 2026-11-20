package com.oopforge.example.calculator.domain

class Calculation private constructor(
    val id: CalculationId,
    val operandA: Double,
    val operator: Operator,
    val operandB: Double,
    val result: Double,
) {
    private val events: MutableList<DomainEvent> = mutableListOf()

    fun popEvents(): List<DomainEvent> = TODO("Implement stage")

    companion object {
        fun perform(id: CalculationId, operandA: Double, operator: Operator, operandB: Double): Calculation =
            TODO("Implement stage")
    }
}
