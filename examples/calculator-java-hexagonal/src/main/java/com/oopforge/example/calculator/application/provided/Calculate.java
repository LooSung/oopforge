package com.oopforge.example.calculator.application.provided;

import com.oopforge.example.calculator.domain.Operator;

public interface Calculate {

    CalculationResult handle(CalculateCommand command);

    record CalculateCommand(double operandA, Operator operator, double operandB) {}

    record CalculationResult(String calculationId, double operandA, Operator operator, double operandB, double result) {}
}
