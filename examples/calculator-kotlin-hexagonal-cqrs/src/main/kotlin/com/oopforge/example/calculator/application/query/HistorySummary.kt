package com.oopforge.example.calculator.application.query

import com.oopforge.example.calculator.domain.Calculation
import java.time.Instant

/**
 * Read model — denormalized projection for the query side, not a domain object.
 */
data class HistorySummary(
    val calculationId: String,
    val operandA: Double,
    val operandB: Double,
    val operator: String,
    val result: Double,
    val performedAt: Instant,
) {
    companion object {
        fun from(calculation: Calculation): HistorySummary = TODO("Implement stage")
    }
}
