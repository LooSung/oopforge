package com.oopforge.example.calculator.domain;

import java.util.Objects;
import java.util.UUID;

public record CalculationId(UUID value) {

    public CalculationId {
        Objects.requireNonNull(value, "value");
    }

    public static CalculationId generate() {
        return new CalculationId(UUID.randomUUID());
    }

    public static CalculationId of(String raw) {
        return new CalculationId(UUID.fromString(raw));
    }
}
