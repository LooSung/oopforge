package com.oopforge.example.calculator.application.query

import com.oopforge.example.calculator.domain.CalculationId

/**
 * Inbound query port (read side) — read-only, returns projections.
 */
interface CalculationHistory {

    fun listRecent(limit: Int): List<HistorySummary>

    fun findById(calculationId: CalculationId): HistorySummary?
}
