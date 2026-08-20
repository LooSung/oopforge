package com.oopforge.example.calculator.application.service;

import com.oopforge.example.calculator.application.provided.Calculate;
import com.oopforge.example.calculator.application.required.CalculationRepository;
import com.oopforge.example.calculator.application.required.DomainEventDispatcher;
import com.oopforge.example.calculator.application.required.TransactionRunner;
import com.oopforge.example.calculator.domain.Calculation;
import com.oopforge.example.calculator.domain.CalculationId;

public class CalculateService implements Calculate {

    private final CalculationRepository calculationRepository;
    private final TransactionRunner transactionRunner;
    private final DomainEventDispatcher eventDispatcher;

    public CalculateService(
            CalculationRepository calculationRepository,
            TransactionRunner transactionRunner,
            DomainEventDispatcher eventDispatcher) {
        this.calculationRepository = calculationRepository;
        this.transactionRunner = transactionRunner;
        this.eventDispatcher = eventDispatcher;
    }

    @Override
    public CalculationResult handle(CalculateCommand command) {
        return transactionRunner.run(() -> calculate(command));
    }

    private CalculationResult calculate(CalculateCommand command) {
        CalculationId id = CalculationId.generate();
        Calculation calculation = Calculation.perform(id, command.operandA(), command.operator(), command.operandB());
        calculationRepository.save(calculation);
        eventDispatcher.dispatch(calculation.popEvents());
        return new CalculationResult(
                id.value().toString(),
                calculation.operandA(),
                calculation.operator(),
                calculation.operandB(),
                calculation.result());
    }
}
