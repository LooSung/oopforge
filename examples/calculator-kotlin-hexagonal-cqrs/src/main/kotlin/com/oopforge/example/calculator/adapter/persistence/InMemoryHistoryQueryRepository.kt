package com.oopforge.example.calculator.adapter.persistence

import com.oopforge.example.calculator.application.query.HistoryQueryRepository
import com.oopforge.example.calculator.application.query.HistorySummary
import com.oopforge.example.calculator.domain.CalculationId

/**
 * Read adapter: serves projections from the store, most-recent first.
 */
class InMemoryHistoryQueryRepository(private val store: CalculationStore) : HistoryQueryRepository {

    override fun listRecent(limit: Int): List<HistorySummary> = TODO("Implement stage")

    override fun findById(calculationId: CalculationId): HistorySummary? = TODO("Implement stage")
}
