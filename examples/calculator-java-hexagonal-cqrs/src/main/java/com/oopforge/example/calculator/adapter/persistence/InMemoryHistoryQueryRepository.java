package com.oopforge.example.calculator.adapter.persistence;

import com.oopforge.example.calculator.application.query.HistoryQueryRepository;
import com.oopforge.example.calculator.application.query.HistorySummary;
import com.oopforge.example.calculator.domain.CalculationId;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Optional;

/**
 * Read adapter: serves projections from the store, most-recent first.
 */
public class InMemoryHistoryQueryRepository implements HistoryQueryRepository {

    private final CalculationStore store;

    public InMemoryHistoryQueryRepository(CalculationStore store) {
        this.store = store;
    }

    @Override
    public List<HistorySummary> listRecent(int limit) {
        if (limit <= 0) {
            throw new IllegalArgumentException("limit must be positive");
        }
        List<HistorySummary> all = store.historySnapshot();
        int from = Math.max(0, all.size() - limit);
        List<HistorySummary> tail = new ArrayList<>(all.subList(from, all.size()));
        Collections.reverse(tail);
        return List.copyOf(tail);
    }

    @Override
    public Optional<HistorySummary> findById(CalculationId calculationId) {
        String target = calculationId.value().toString();
        List<HistorySummary> all = store.historySnapshot();
        for (int i = all.size() - 1; i >= 0; i--) {
            if (all.get(i).calculationId().equals(target)) {
                return Optional.of(all.get(i));
            }
        }
        return Optional.empty();
    }
}
