package com.oopforge.example.calculator.domain

class CalculationPerformed(
    val calculationId: CalculationId,
    val result: Double,
) : DomainEvent()
