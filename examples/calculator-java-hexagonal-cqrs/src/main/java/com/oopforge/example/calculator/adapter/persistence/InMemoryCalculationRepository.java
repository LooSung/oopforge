package com.oopforge.example.calculator.adapter.persistence;

import com.oopforge.example.calculator.application.command.CalculationRepository;
import com.oopforge.example.calculator.application.query.HistorySummary;
import com.oopforge.example.calculator.domain.Calculation;

/**
 * Write adapter: persists the aggregate and projects the read model.
 */
public class InMemoryCalculationRepository implements CalculationRepository {

    private final CalculationStore store;

    public InMemoryCalculationRepository(CalculationStore store) {
        this.store = store;
    }

    @Override
    public void save(Calculation calculation) {
        store.putCalculation(calculation);
        store.appendHistory(HistorySummary.from(calculation));
    }
}
