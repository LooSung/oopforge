package com.oopforge.example.calculator.adapter.web;

import com.oopforge.example.calculator.application.provided.Calculate;
import org.springframework.stereotype.Component;

@Component
final class IdempotentCalculationHandler {

    private final Calculate calculate;
    private final IdempotencyStore idempotencyStore;

    IdempotentCalculationHandler(Calculate calculate, IdempotencyStore idempotencyStore) {
        this.calculate = calculate;
        this.idempotencyStore = idempotencyStore;
    }

    CalculationResponse handle(CalculateRequest request, String idempotencyKey) {
        NormalizedRequest normalized = NormalizedRequest.from(request);
        return idempotencyStore.execute(
                idempotencyKey,
                normalized,
                () -> perform(normalized));
    }

    private CalculationResponse perform(NormalizedRequest request) {
        Calculate.CalculationResult result = calculate.handle(new Calculate.CalculateCommand(
                request.operandA(), request.operator(), request.operandB()));
        return new CalculationResponse(
                result.calculationId(),
                result.operandA(),
                result.operator().name().toLowerCase(),
                result.operandB(),
                result.result());
    }
}
