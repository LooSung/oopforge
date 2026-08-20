package com.oopforge.example.calculator.application.service;

import com.oopforge.example.calculator.application.integration.CalculationPerformedV1;
import com.oopforge.example.calculator.application.required.OutboxMessage;
import com.oopforge.example.calculator.application.required.OutboxPort;
import com.oopforge.example.calculator.domain.CalculationPerformed;

public final class CalculationPerformedHandler implements DomainEventHandler<CalculationPerformed> {

    private final OutboxPort outbox;

    public CalculationPerformedHandler(OutboxPort outbox) {
        this.outbox = outbox;
    }

    @Override
    public Class<CalculationPerformed> eventType() {
        return CalculationPerformed.class;
    }

    @Override
    public void handle(CalculationPerformed event) {
        CalculationPerformedV1 payload = new CalculationPerformedV1(
                CalculationPerformedV1.SCHEMA_VERSION,
                event.calculationId().value().toString(),
                event.result(),
                event.occurredAt());
        outbox.append(new OutboxMessage(
                event.eventId(),
                payload.calculationId(),
                CalculationPerformedV1.class.getSimpleName(),
                payload,
                event.occurredAt()));
    }
}
