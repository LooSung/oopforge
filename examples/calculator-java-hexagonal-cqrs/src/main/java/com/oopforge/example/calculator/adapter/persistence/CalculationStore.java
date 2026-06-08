package com.oopforge.example.calculator.adapter.persistence;

import com.oopforge.example.calculator.application.query.HistorySummary;
import com.oopforge.example.calculator.domain.Calculation;
import com.oopforge.example.calculator.domain.CalculationId;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CopyOnWriteArrayList;

/**
 * Shared in-memory backing store: write model (aggregates) + read projection
 * (history). Both adapters depend on this one store so a command is visible to
 * later queries.
 */
public class CalculationStore {

    private final Map<CalculationId, Calculation> calculations = new ConcurrentHashMap<>();
    private final List<HistorySummary> history = new CopyOnWriteArrayList<>();

    public void putCalculation(Calculation calculation) {
        calculations.put(calculation.id(), calculation);
    }

    public void appendHistory(HistorySummary summary) {
        history.add(summary);
    }

    public List<HistorySummary> historySnapshot() {
        return List.copyOf(history);
    }
}
