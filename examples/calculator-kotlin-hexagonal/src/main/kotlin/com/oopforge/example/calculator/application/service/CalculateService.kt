package com.oopforge.example.calculator.application.service

import com.oopforge.example.calculator.application.provided.Calculate
import com.oopforge.example.calculator.application.provided.Calculate.CalculateCommand
import com.oopforge.example.calculator.application.provided.Calculate.CalculationResult
import com.oopforge.example.calculator.application.required.CalculationRepository
import com.oopforge.example.calculator.application.required.DomainEventDispatcher
import com.oopforge.example.calculator.application.required.TransactionRunner

class CalculateService(
    private val calculationRepository: CalculationRepository,
    private val transactionRunner: TransactionRunner,
    private val eventDispatcher: DomainEventDispatcher,
) : Calculate {

    override fun handle(command: CalculateCommand): CalculationResult = TODO("Implement stage")
}
