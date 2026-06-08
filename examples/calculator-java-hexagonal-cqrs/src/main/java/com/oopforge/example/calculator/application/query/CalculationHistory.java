package com.oopforge.example.calculator.application.query;

import com.oopforge.example.calculator.domain.CalculationId;
import java.util.List;
import java.util.Optional;

/**
 * Inbound query port (read side) — read-only, returns projections.
 */
public interface CalculationHistory {

    List<HistorySummary> listRecent(int limit);

    Optional<HistorySummary> findById(CalculationId calculationId);
}
