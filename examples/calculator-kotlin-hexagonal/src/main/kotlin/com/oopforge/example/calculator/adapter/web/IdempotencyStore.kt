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
    ): CalculationResponse {
        if (key == null) {
            return operation()
        }
        validate(key)
        return synchronized(locks.computeIfAbsent(key) { Any() }) {
            executeLocked(key, request, operation)
        }
    }

    private fun executeLocked(
        key: String,
        request: NormalizedRequest,
        operation: () -> CalculationResponse,
    ): CalculationResponse {
        val stored = results[key]
        if (stored == null) {
            val response = operation()
            results[key] = StoredResult(request, response)
            return response
        }
        if (stored.request != request) {
            throw IdempotencyConflictException()
        }
        return stored.response
    }

    private fun validate(key: String) {
        if (key.all(Character::isWhitespace) || key.length > MAX_KEY_LENGTH) {
            throw InvalidWebRequestException()
        }
    }

    private data class StoredResult(val request: NormalizedRequest, val response: CalculationResponse)

    private companion object {
        const val MAX_KEY_LENGTH: Int = 200
    }
}
