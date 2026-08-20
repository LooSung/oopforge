package com.oopforge.example.calculator.application.integration;

import java.time.Instant;
import java.util.Objects;

public record CalculationPerformedV1(
        int schemaVersion,
        String calculationId,
        double result,
        Instant occurredAt) {

    public static final int SCHEMA_VERSION = 1;

    public CalculationPerformedV1 {
        if (schemaVersion != SCHEMA_VERSION) {
            throw new IllegalArgumentException("schemaVersion must be 1");
        }
        Objects.requireNonNull(calculationId, "calculationId");
        Objects.requireNonNull(occurredAt, "occurredAt");
    }
}
