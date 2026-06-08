package com.oopforge.example.calculator.application.query;

import com.oopforge.example.calculator.domain.CalculationId;
import java.util.List;
import java.util.Optional;

/**
 * Read side: only reads projections — no state changes.
 */
public class HistoryQueryService implements CalculationHistory {

    private final HistoryQueryRepository queryRepository;

    public HistoryQueryService(HistoryQueryRepository queryRepository) {
        this.queryRepository = queryRepository;
    }

    @Override
    public List<HistorySummary> listRecent(int limit) {
        return queryRepository.listRecent(limit);
    }

    @Override
    public Optional<HistorySummary> findById(CalculationId calculationId) {
        return queryRepository.findById(calculationId);
    }
}
