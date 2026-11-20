package com.oopforge.example.calculator.application.query

import com.oopforge.example.calculator.domain.CalculationId

/**
 * Read side: only reads projections — no state changes.
 */
class HistoryQueryService(private val queryRepository: HistoryQueryRepository) : CalculationHistory {

    override fun listRecent(limit: Int): List<HistorySummary> = queryRepository.listRecent(limit)

    override fun findById(calculationId: CalculationId): HistorySummary? = queryRepository.findById(calculationId)
}
