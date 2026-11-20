package com.oopforge.example.calculator.application.command

import com.oopforge.example.calculator.domain.CalculationId
import com.oopforge.example.calculator.domain.Operator

/**
 * Inbound command port (write side). Returns only the new aggregate's ID —
 * never read-shaped data — keeping the command/query split honest.
 */
interface Calculate {

    fun handle(command: CalculateCommand): CalculationId

    data class CalculateCommand(val operandA: Double, val operator: Operator, val operandB: Double)
}
