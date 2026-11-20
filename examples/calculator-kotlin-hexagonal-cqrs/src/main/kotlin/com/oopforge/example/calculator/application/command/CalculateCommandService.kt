package com.oopforge.example.calculator.application.command

import com.oopforge.example.calculator.domain.Calculation
import com.oopforge.example.calculator.domain.CalculationId

/**
 * Write side: performs a calculation and returns only its ID.
 */
class CalculateCommandService(private val calculationRepository: CalculationRepository) : Calculate {

    override fun handle(command: Calculate.CalculateCommand): CalculationId {
        val id = CalculationId.generate()
        val calculation = Calculation.perform(id, command.operandA, command.operator, command.operandB)
        calculationRepository.save(calculation)
        return id
    }
}
