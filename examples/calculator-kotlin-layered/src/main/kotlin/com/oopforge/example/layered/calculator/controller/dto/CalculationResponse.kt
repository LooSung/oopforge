package com.oopforge.example.layered.calculator.controller.dto

data class CalculationResponse(
    val calculationId: String,
    val operandA: Double,
    val operator: String,
    val operandB: Double,
    val result: Double,
)
