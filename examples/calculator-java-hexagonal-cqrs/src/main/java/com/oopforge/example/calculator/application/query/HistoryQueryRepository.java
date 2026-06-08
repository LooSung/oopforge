package com.oopforge.example.calculator.application.query;

import com.oopforge.example.calculator.domain.CalculationId;
import java.util.List;
import java.util.Optional;

/**
 * Outbound read port (query side) — returns read models, never aggregates.
 */
public interface HistoryQueryRepository {

    List<HistorySummary> listRecent(int limit);

    Optional<HistorySummary> findById(CalculationId calculationId);
}
