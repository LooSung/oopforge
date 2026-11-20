package com.oopforge.example.calculator.application.query

import com.oopforge.example.calculator.domain.CalculationId

/**
 * Outbound read port (query side) — returns read models, never aggregates.
 */
interface HistoryQueryRepository {

    fun listRecent(limit: Int): List<HistorySummary>

    fun findById(calculationId: CalculationId): HistorySummary?
}
