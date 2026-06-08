package com.oopforge.example.calculator.adapter.web;

import com.oopforge.example.calculator.application.query.HistorySummary;

public record HistoryEntryResponse(
        String calculationId,
        double operandA,
        double operandB,
        String operator,
        double result,
        String performedAt) {

    public static HistoryEntryResponse from(HistorySummary summary) {
        return new HistoryEntryResponse(
                summary.calculationId(),
                summary.operandA(),
                summary.operandB(),
                summary.operator(),
                summary.result(),
                summary.performedAt().toString());
    }
}
