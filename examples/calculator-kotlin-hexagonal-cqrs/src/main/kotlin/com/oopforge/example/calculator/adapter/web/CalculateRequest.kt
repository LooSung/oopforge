package com.oopforge.example.calculator.adapter.web

import com.oopforge.example.calculator.domain.Operator

data class CalculateRequest(val operandA: Double, val operator: Operator, val operandB: Double)
