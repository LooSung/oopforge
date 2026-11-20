package com.oopforge.example.calculator.adapter.web

import com.oopforge.example.calculator.domain.Operator

internal data class NormalizedRequest(val operandA: Double, val operator: Operator, val operandB: Double) {

    companion object {
        fun from(request: CalculateRequest): NormalizedRequest = TODO("Implement stage")
    }
}
