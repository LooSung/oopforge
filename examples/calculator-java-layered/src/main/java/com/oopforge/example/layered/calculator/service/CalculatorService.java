package com.oopforge.example.layered.calculator.service;

import com.oopforge.example.layered.calculator.domain.Calculation;
import com.oopforge.example.layered.calculator.domain.CalculationId;
import com.oopforge.example.layered.calculator.domain.Operator;
import com.oopforge.example.layered.calculator.repository.CalculationRepository;
import org.springframework.stereotype.Service;

@Service
public class CalculatorService {

    private final CalculationRepository calculationRepository;

    public CalculatorService(CalculationRepository calculationRepository) {
        this.calculationRepository = calculationRepository;
    }

    public CalculationResult calculate(CalculateCommand command) {
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

    public record CalculateCommand(double operandA, Operator operator, double operandB) {}

    public record CalculationResult(String calculationId, double operandA, Operator operator, double operandB, double result) {}
}
