package com.oopforge.example.calculator.application.command;

import com.oopforge.example.calculator.domain.Calculation;
import com.oopforge.example.calculator.domain.CalculationId;

/**
 * Write side: performs a calculation and returns only its ID.
 */
public class CalculateCommandService implements Calculate {

    private final CalculationRepository calculationRepository;

    public CalculateCommandService(CalculationRepository calculationRepository) {
        this.calculationRepository = calculationRepository;
    }

    @Override
    public CalculationId handle(CalculateCommand command) {
        CalculationId id = CalculationId.generate();
        Calculation calculation = Calculation.perform(id, command.operandA(), command.operator(), command.operandB());
        calculationRepository.save(calculation);
        calculation.popEvents();
        return id;
    }
}
