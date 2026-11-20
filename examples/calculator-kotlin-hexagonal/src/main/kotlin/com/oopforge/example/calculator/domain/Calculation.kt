package com.oopforge.example.calculator.domain

class Calculation private constructor(
    val id: CalculationId,
    val operandA: Double,
    val operator: Operator,
    val operandB: Double,
    val result: Double,
) {
    private val events: MutableList<DomainEvent> = mutableListOf()

    fun popEvents(): List<DomainEvent> {
        val published = events.toList()
        events.clear()
        return published
    }

    private fun record(event: DomainEvent) {
        events.add(event)
    }

    companion object {
        fun perform(id: CalculationId, operandA: Double, operator: Operator, operandB: Double): Calculation {
            val result = operator.apply(operandA, operandB)
            val calculation = Calculation(id, operandA, operator, operandB, result)
            calculation.record(CalculationPerformed(id, result))
            return calculation
        }
    }
}
