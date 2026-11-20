package com.oopforge.example.calculator.adapter.web

import com.oopforge.example.calculator.application.provided.Calculate
import org.springframework.stereotype.Component

@Component
internal class IdempotentCalculationHandler(
    private val calculate: Calculate,
    private val idempotencyStore: IdempotencyStore,
) {

    fun handle(request: CalculateRequest, idempotencyKey: String?): CalculationResponse {
        val normalized = NormalizedRequest.from(request)
        return idempotencyStore.execute(idempotencyKey, normalized) { perform(normalized) }
    }

    private fun perform(request: NormalizedRequest): CalculationResponse {
        val result = calculate.handle(
            Calculate.CalculateCommand(request.operandA, request.operator, request.operandB),
        )
        return CalculationResponse(
            result.calculationId,
            result.operandA,
            result.operator.name.lowercase(),
            result.operandB,
            result.result,
        )
    }
}
