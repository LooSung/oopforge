package com.oopforge.example.calculator.application.command;

import com.oopforge.example.calculator.domain.CalculationId;
import com.oopforge.example.calculator.domain.Operator;

/**
 * Inbound command port (write side). Returns only the new aggregate's ID —
 * never read-shaped data — keeping the command/query split honest.
 */
public interface Calculate {

    CalculationId handle(CalculateCommand command);

    record CalculateCommand(double operandA, Operator operator, double operandB) {}
}
