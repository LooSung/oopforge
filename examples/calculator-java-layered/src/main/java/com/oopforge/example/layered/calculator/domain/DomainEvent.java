package com.oopforge.example.layered.calculator.domain;

import java.time.Instant;
import java.util.UUID;

public abstract class DomainEvent {

    private final UUID eventId;
    private final Instant occurredAt;

    protected DomainEvent() {
        this.eventId = UUID.randomUUID();
        this.occurredAt = Instant.now();
    }

    public UUID eventId() {
        return eventId;
    }

    public Instant occurredAt() {
        return occurredAt;
    }
}
