package com.oopforge.example.calculator.adapter.web

import com.oopforge.example.calculator.application.provided.Calculate
import org.springframework.stereotype.Component

@Component
internal class IdempotentCalculationHandler(
    private val calculate: Calculate,
    private val idempotencyStore: IdempotencyStore,
) {

    fun handle(request: CalculateRequest, idempotencyKey: String?): CalculationResponse = TODO("Implement stage")
}
