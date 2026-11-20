package com.oopforge.example.calculator.application.command

import com.oopforge.example.calculator.domain.CalculationId

/**
 * Write side: performs a calculation and returns only its ID.
 */
class CalculateCommandService(private val calculationRepository: CalculationRepository) : Calculate {

    override fun handle(command: Calculate.CalculateCommand): CalculationId = TODO("Implement stage")
}
