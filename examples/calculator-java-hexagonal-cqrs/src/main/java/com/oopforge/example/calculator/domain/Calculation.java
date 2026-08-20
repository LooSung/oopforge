package com.oopforge.example.calculator.domain;

import java.time.Instant;
import java.util.Objects;

public final class Calculation {

    private final CalculationId id;
    private final double operandA;
    private final Operator operator;
    private final double operandB;
    private final double result;
    private final Instant performedAt;

    private Calculation(CalculationId id, double operandA, Operator operator,
                        double operandB, double result, Instant performedAt) {
        this.id = id;
        this.operandA = operandA;
        this.operator = operator;
        this.operandB = operandB;
        this.result = result;
        this.performedAt = performedAt;
    }

    public static Calculation perform(CalculationId id, double operandA, Operator operator, double operandB) {
        Objects.requireNonNull(id, "id");
        Objects.requireNonNull(operator, "operator");

        double result = operator.apply(operandA, operandB);
        return new Calculation(id, operandA, operator, operandB, result, Instant.now());
    }

    public CalculationId id() {
        return id;
    }

    public double operandA() {
        return operandA;
    }

    public Operator operator() {
        return operator;
    }

    public double operandB() {
        return operandB;
    }

    public double result() {
        return result;
    }

    public Instant performedAt() {
        return performedAt;
    }
}
