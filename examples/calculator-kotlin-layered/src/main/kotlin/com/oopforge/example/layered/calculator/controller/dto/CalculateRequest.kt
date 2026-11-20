package com.oopforge.example.layered.calculator.controller.dto

import com.oopforge.example.layered.calculator.domain.Operator

data class CalculateRequest(val operandA: Double, val operator: Operator, val operandB: Double)
