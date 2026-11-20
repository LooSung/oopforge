package com.oopforge.example.layered.calculator.service

import com.oopforge.example.layered.calculator.domain.Calculation
import com.oopforge.example.layered.calculator.domain.CalculationId
import com.oopforge.example.layered.calculator.domain.Operator
import com.oopforge.example.layered.calculator.repository.CalculationRepository
import org.springframework.stereotype.Service

@Service
class CalculatorService(private val calculationRepository: CalculationRepository) {

    fun calculate(command: CalculateCommand): CalculationResult {
        val id = CalculationId.generate()
        val calculation = Calculation.perform(id, command.operandA, command.operator, command.operandB)
        calculationRepository.save(calculation)
        return CalculationResult(
            id.value.toString(),
            calculation.operandA,
            calculation.operator,
            calculation.operandB,
            calculation.result,
        )
    }

    data class CalculateCommand(val operandA: Double, val operator: Operator, val operandB: Double)

    data class CalculationResult(
        val calculationId: String,
        val operandA: Double,
        val operator: Operator,
        val operandB: Double,
        val result: Double,
    )
}
