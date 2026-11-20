package com.oopforge.example.calculator.adapter.messaging

import com.oopforge.example.calculator.application.required.OutboxPort
import java.time.Instant

class OutboxRelay(
    private val outbox: OutboxPort,
    private val consumer: OutboxConsumer,
) {

    fun relay() {
        for (message in outbox.unpublished()) {
            consumer.consume(message)
            outbox.markPublished(message.id, Instant.now())
        }
    }
}
