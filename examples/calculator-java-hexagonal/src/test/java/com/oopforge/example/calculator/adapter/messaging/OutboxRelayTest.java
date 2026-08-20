package com.oopforge.example.calculator.adapter.messaging;

import com.oopforge.example.calculator.adapter.persistence.InMemoryTransactionalAdapter;
import com.oopforge.example.calculator.application.integration.CalculationPerformedV1;
import com.oopforge.example.calculator.application.required.OutboxMessage;
import org.junit.jupiter.api.Test;

import java.time.Instant;
import java.util.UUID;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

class OutboxRelayTest {

    @Test
    void leavesMessageUnpublishedWhenConsumerFails() {
        InMemoryTransactionalAdapter store = new InMemoryTransactionalAdapter();
        OutboxMessage message = message();
        store.run(() -> {
            store.append(message);
            return null;
        });
        OutboxRelay relay = new OutboxRelay(store, ignored -> {
            throw new IllegalStateException("consumer failed");
        });

        assertThatThrownBy(relay::relay).isInstanceOf(IllegalStateException.class);

        assertThat(store.unpublished()).containsExactly(message);
        assertThat(store.publishedAt(message.id())).isEmpty();
    }

    private OutboxMessage message() {
        Instant occurredAt = Instant.parse("2026-08-20T00:00:00Z");
        CalculationPerformedV1 payload =
                new CalculationPerformedV1(1, UUID.randomUUID().toString(), 4, occurredAt);
        return new OutboxMessage(
                UUID.randomUUID(),
                payload.calculationId(),
                CalculationPerformedV1.class.getSimpleName(),
                payload,
                occurredAt);
    }
}
