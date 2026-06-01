package com.oopforge.example.layered.order.domain;

import java.time.Instant;
import java.util.UUID;

public abstract class DomainEvent {

    private final String eventId;
    private final Instant occurredAt;

    protected DomainEvent() {
        this.eventId = UUID.randomUUID().toString();
        this.occurredAt = Instant.now();
    }

    public String eventId() {
        return eventId;
    }

    public Instant occurredAt() {
        return occurredAt;
    }
}
