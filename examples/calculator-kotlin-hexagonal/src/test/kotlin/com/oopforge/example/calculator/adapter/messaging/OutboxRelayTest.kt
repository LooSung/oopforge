package com.oopforge.example.calculator.adapter.messaging

import com.oopforge.example.calculator.adapter.persistence.InMemoryTransactionalAdapter
import com.oopforge.example.calculator.application.integration.CalculationPerformedV1
import com.oopforge.example.calculator.application.required.OutboxMessage
import org.assertj.core.api.Assertions.assertThat
import org.assertj.core.api.Assertions.assertThatThrownBy
import org.junit.jupiter.api.Test
import java.time.Instant
import java.util.UUID

class OutboxRelayTest {

    @Test
    fun leavesMessageUnpublishedWhenConsumerFails() {
        val store = InMemoryTransactionalAdapter()
        val message = message()
        store.run { store.append(message) }
        val relay = OutboxRelay(store) { throw IllegalStateException("consumer failed") }

        assertThatThrownBy(relay::relay).isInstanceOf(IllegalStateException::class.java)

        assertThat(store.unpublished()).containsExactly(message)
        assertThat(store.publishedAt(message.id)).isNull()
    }

    private fun message(): OutboxMessage {
        val occurredAt = Instant.parse("2026-08-20T00:00:00Z")
        val payload = CalculationPerformedV1(1, UUID.randomUUID().toString(), 4.0, occurredAt)
        return OutboxMessage(
            UUID.randomUUID(),
            payload.calculationId,
            CalculationPerformedV1::class.java.simpleName,
            payload,
            occurredAt,
        )
    }
}
