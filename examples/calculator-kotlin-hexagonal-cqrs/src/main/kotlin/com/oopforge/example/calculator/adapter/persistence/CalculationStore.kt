package com.oopforge.example.calculator.adapter.persistence

import com.oopforge.example.calculator.application.query.HistorySummary
import com.oopforge.example.calculator.domain.Calculation
import com.oopforge.example.calculator.domain.CalculationId
import java.util.concurrent.ConcurrentHashMap
import java.util.concurrent.CopyOnWriteArrayList

/**
 * Shared in-memory backing store: write model (aggregates) + read projection
 * (history). Both adapters depend on this one store so a command is visible to
 * later queries.
 */
class CalculationStore {

    private val calculations = ConcurrentHashMap<CalculationId, Calculation>()
    private val history = CopyOnWriteArrayList<HistorySummary>()

    fun putCalculation(calculation: Calculation) {
        TODO("Implement stage")
    }

    fun appendHistory(summary: HistorySummary) {
        TODO("Implement stage")
    }

    fun historySnapshot(): List<HistorySummary> = TODO("Implement stage")
}
