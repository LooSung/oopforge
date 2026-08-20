package com.oopforge.example.calculator.application.required;

import java.time.Instant;
import java.util.Objects;
import java.util.UUID;

public record OutboxMessage(
        UUID id,
        String aggregateId,
        String eventType,
        Object payload,
        Instant occurredAt) {

    public OutboxMessage {
        Objects.requireNonNull(id, "id");
        Objects.requireNonNull(aggregateId, "aggregateId");
        Objects.requireNonNull(eventType, "eventType");
        Objects.requireNonNull(payload, "payload");
        Objects.requireNonNull(occurredAt, "occurredAt");
    }
}
