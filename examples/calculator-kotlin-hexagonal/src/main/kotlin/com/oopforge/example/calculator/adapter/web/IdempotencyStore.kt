package com.oopforge.example.calculator.adapter.web

import org.springframework.stereotype.Component
import java.util.concurrent.ConcurrentHashMap

@Component
internal class IdempotencyStore {

    private val results = ConcurrentHashMap<String, StoredResult>()
    private val locks = ConcurrentHashMap<String, Any>()

    fun execute(
        key: String?,
        request: NormalizedRequest,
        operation: () -> CalculationResponse,
    ): CalculationResponse = TODO("Implement stage")

    private data class StoredResult(val request: NormalizedRequest, val response: CalculationResponse)

    private companion object {
        const val MAX_KEY_LENGTH: Int = 200
    }
}
