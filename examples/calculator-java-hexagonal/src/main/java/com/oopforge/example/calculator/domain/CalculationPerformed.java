package com.oopforge.example.calculator.domain;

public final class CalculationPerformed extends DomainEvent {

    private final CalculationId calculationId;
    private final double result;

    public CalculationPerformed(CalculationId calculationId, double result) {
        super();
        this.calculationId = calculationId;
        this.result = result;
    }

    public CalculationId calculationId() {
        return calculationId;
    }

    public double result() {
        return result;
    }
}
