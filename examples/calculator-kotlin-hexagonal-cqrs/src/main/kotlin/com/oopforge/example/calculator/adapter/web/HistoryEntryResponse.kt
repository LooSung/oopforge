package com.oopforge.example.calculator.adapter.web

import com.oopforge.example.calculator.application.query.HistorySummary

data class HistoryEntryResponse(
    val calculationId: String,
    val operandA: Double,
    val operandB: Double,
    val operator: String,
    val result: Double,
    val performedAt: String,
) {
    companion object {
        fun from(summary: HistorySummary): HistoryEntryResponse = TODO("Implement stage")
    }
}
