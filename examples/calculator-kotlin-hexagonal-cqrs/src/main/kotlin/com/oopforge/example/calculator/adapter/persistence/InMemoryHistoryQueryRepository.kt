package com.oopforge.example.calculator.adapter.persistence

import com.oopforge.example.calculator.application.query.HistoryQueryRepository
import com.oopforge.example.calculator.application.query.HistorySummary
import com.oopforge.example.calculator.domain.CalculationId

/**
 * Read adapter: serves projections from the store, most-recent first.
 */
class InMemoryHistoryQueryRepository(private val store: CalculationStore) : HistoryQueryRepository {

    override fun listRecent(limit: Int): List<HistorySummary> {
        require(limit > 0) { "limit must be positive" }
        return store.historySnapshot().takeLast(limit).reversed()
    }

    override fun findById(calculationId: CalculationId): HistorySummary? {
        val target = calculationId.value.toString()
        return store.historySnapshot().lastOrNull { it.calculationId == target }
    }
}
