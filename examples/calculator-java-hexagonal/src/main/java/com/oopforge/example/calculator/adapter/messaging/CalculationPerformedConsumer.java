package com.oopforge.example.calculator.adapter.messaging;

import com.oopforge.example.calculator.application.integration.CalculationPerformedV1;
import com.oopforge.example.calculator.application.required.OutboxMessage;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.UUID;

public final class CalculationPerformedConsumer implements OutboxConsumer {

    private final Set<UUID> processedMessageIds = new HashSet<>();
    private final List<CalculationPerformedV1> effects = new ArrayList<>();

    @Override
    public synchronized void consume(OutboxMessage message) {
        CalculationPerformedV1 payload = payloadOf(message);
        if (processedMessageIds.contains(message.id())) {
            return;
        }
        effects.add(payload);
        processedMessageIds.add(message.id());
    }

    public synchronized List<CalculationPerformedV1> effects() {
        return List.copyOf(effects);
    }

    private CalculationPerformedV1 payloadOf(OutboxMessage message) {
        if (message.payload() instanceof CalculationPerformedV1 payload) {
            return payload;
        }
        throw new IllegalArgumentException("unsupported outbox payload");
    }
}
