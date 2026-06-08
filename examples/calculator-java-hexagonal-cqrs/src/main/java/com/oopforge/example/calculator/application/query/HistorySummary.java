package com.oopforge.example.calculator.application.query;

import com.oopforge.example.calculator.domain.Calculation;
import java.time.Instant;

/**
 * Read model — denormalized projection for the query side, not a domain object.
 */
public record HistorySummary(
        String calculationId,
        double operandA,
        double operandB,
        String operator,
        double result,
        Instant performedAt) {

    public static HistorySummary from(Calculation calculation) {
        return new HistorySummary(
                calculation.id().value().toString(),
                calculation.operandA(),
                calculation.operandB(),
                calculation.operator().name().toLowerCase(),
                calculation.result(),
                calculation.performedAt());
    }
}
