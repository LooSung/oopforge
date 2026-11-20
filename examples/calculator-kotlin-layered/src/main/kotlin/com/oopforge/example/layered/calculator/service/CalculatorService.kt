package com.oopforge.example.layered.calculator.service

import com.oopforge.example.layered.calculator.domain.Operator
import com.oopforge.example.layered.calculator.repository.CalculationRepository
import org.springframework.stereotype.Service

@Service
class CalculatorService(private val calculationRepository: CalculationRepository) {

    fun calculate(command: CalculateCommand): CalculationResult = TODO("Implement stage")

    data class CalculateCommand(val operandA: Double, val operator: Operator, val operandB: Double)

    data class CalculationResult(
        val calculationId: String,
        val operandA: Double,
        val operator: Operator,
        val operandB: Double,
        val result: Double,
    )
}
