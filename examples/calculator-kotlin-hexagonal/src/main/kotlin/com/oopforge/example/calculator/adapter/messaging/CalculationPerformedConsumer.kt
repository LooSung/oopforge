package com.oopforge.example.calculator.adapter.messaging

import com.oopforge.example.calculator.application.integration.CalculationPerformedV1
import com.oopforge.example.calculator.application.required.OutboxMessage
import java.util.UUID

class CalculationPerformedConsumer : OutboxConsumer {

    private val processedMessageIds: MutableSet<UUID> = mutableSetOf()
    private val effects: MutableList<CalculationPerformedV1> = mutableListOf()

    @Synchronized
    override fun consume(message: OutboxMessage) {
        val payload = payloadOf(message)
        if (message.id in processedMessageIds) {
            return
        }
        effects.add(payload)
        processedMessageIds.add(message.id)
    }

    @Synchronized
    fun effects(): List<CalculationPerformedV1> = effects.toList()

    private fun payloadOf(message: OutboxMessage): CalculationPerformedV1 =
        requireNotNull(message.payload as? CalculationPerformedV1) { "unsupported outbox payload" }
}
