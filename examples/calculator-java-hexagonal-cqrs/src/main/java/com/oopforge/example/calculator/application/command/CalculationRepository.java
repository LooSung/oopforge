package com.oopforge.example.calculator.application.command;

import com.oopforge.example.calculator.domain.Calculation;

/**
 * Outbound write port (command side) — persists the aggregate.
 */
public interface CalculationRepository {

    void save(Calculation calculation);
}
