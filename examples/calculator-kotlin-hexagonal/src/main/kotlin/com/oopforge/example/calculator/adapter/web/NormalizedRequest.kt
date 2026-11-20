package com.oopforge.example.calculator.adapter.web

import com.oopforge.example.calculator.domain.Operator

internal data class NormalizedRequest(val operandA: Double, val operator: Operator, val operandB: Double) {

    companion object {
        fun from(request: CalculateRequest): NormalizedRequest =
            NormalizedRequest(
                normalizeZero(checkNotNull(request.operandA)),
                checkNotNull(request.operator),
                normalizeZero(checkNotNull(request.operandB)),
            )

        private fun normalizeZero(value: Double): Double = if (value == 0.0) 0.0 else value
    }
}
