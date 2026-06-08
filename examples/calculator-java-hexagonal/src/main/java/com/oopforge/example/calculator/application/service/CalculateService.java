package com.oopforge.example.calculator.application.service;

import com.oopforge.example.calculator.application.provided.Calculate;
import com.oopforge.example.calculator.application.required.CalculationRepository;
import com.oopforge.example.calculator.domain.Calculation;
import com.oopforge.example.calculator.domain.CalculationId;

public class CalculateService implements Calculate {

    private final CalculationRepository calculationRepository;

    public CalculateService(CalculationRepository calculationRepository) {
        this.calculationRepository = calculationRepository;
    }

    @Override
    public CalculationResult handle(CalculateCommand command) {
        CalculationId id = CalculationId.generate();
        Calculation calculation = Calculation.perform(id, command.operandA(), command.operator(), command.operandB());
        calculationRepository.save(calculation);
        calculation.popEvents();
        return new CalculationResult(
                id.value().toString(),
                calculation.operandA(),
                calculation.operator(),
                calculation.operandB(),
                calculation.result());
    }
}
