package com.oopforge.example.calculator.adapter.web

data class CalculationResponse(
    val calculationId: String,
    val operandA: Double,
    val operator: String,
    val operandB: Double,
    val result: Double,
)
