package com.oopforge.example.calculator.adapter.messaging;

import com.oopforge.example.calculator.application.required.OutboxMessage;
import com.oopforge.example.calculator.application.required.OutboxPort;

import java.time.Instant;

public final class OutboxRelay {

    private final OutboxPort outbox;
    private final OutboxConsumer consumer;

    public OutboxRelay(OutboxPort outbox, OutboxConsumer consumer) {
        this.outbox = outbox;
        this.consumer = consumer;
    }

    public void relay() {
        for (OutboxMessage message : outbox.unpublished()) {
            consumer.consume(message);
            outbox.markPublished(message.id(), Instant.now());
        }
    }
}
