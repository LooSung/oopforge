package com.oopforge.example.calculator.application.service

import com.oopforge.example.calculator.application.provided.Calculate
import com.oopforge.example.calculator.application.provided.Calculate.CalculateCommand
import com.oopforge.example.calculator.application.provided.Calculate.CalculationResult
import com.oopforge.example.calculator.application.required.CalculationRepository
import com.oopforge.example.calculator.application.required.DomainEventDispatcher
import com.oopforge.example.calculator.application.required.TransactionRunner
import com.oopforge.example.calculator.domain.Calculation
import com.oopforge.example.calculator.domain.CalculationId

class CalculateService(
    private val calculationRepository: CalculationRepository,
    private val transactionRunner: TransactionRunner,
    private val eventDispatcher: DomainEventDispatcher,
) : Calculate {

    override fun handle(command: CalculateCommand): CalculationResult =
        transactionRunner.run { calculate(command) }

    private fun calculate(command: CalculateCommand): CalculationResult {
        val id = CalculationId.generate()
        val calculation = Calculation.perform(id, command.operandA, command.operator, command.operandB)
        calculationRepository.save(calculation)
        eventDispatcher.dispatch(calculation.popEvents())
        return CalculationResult(
            id.value.toString(),
            calculation.operandA,
            calculation.operator,
            calculation.operandB,
            calculation.result,
        )
    }
}
