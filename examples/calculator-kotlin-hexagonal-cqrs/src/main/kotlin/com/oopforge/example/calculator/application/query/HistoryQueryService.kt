package com.oopforge.example.calculator.application.query

import com.oopforge.example.calculator.domain.CalculationId

/**
 * Read side: only reads projections — no state changes.
 */
class HistoryQueryService(private val queryRepository: HistoryQueryRepository) : CalculationHistory {

    override fun listRecent(limit: Int): List<HistorySummary> = TODO("Implement stage")

    override fun findById(calculationId: CalculationId): HistorySummary? = TODO("Implement stage")
}
