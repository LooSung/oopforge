package com.oopforge.example.calculator.domain;

import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

public final class Calculation {

    private final CalculationId id;
    private final double operandA;
    private final Operator operator;
    private final double operandB;
    private final double result;
    private final Instant performedAt;
    private final List<DomainEvent> events = new ArrayList<>();

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
        Calculation calculation = new Calculation(id, operandA, operator, operandB, result, Instant.now());
        calculation.record(new CalculationPerformed(id, result));
        return calculation;
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

    public List<DomainEvent> popEvents() {
        List<DomainEvent> published = List.copyOf(events);
        events.clear();
        return published;
    }

    private void record(DomainEvent event) {
        events.add(event);
    }
}
