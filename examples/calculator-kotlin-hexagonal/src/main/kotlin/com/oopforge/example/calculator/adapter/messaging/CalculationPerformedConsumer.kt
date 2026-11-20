package com.oopforge.example.calculator.adapter.messaging

import com.oopforge.example.calculator.application.integration.CalculationPerformedV1
import com.oopforge.example.calculator.application.required.OutboxMessage
import java.util.UUID

class CalculationPerformedConsumer : OutboxConsumer {

    private val processedMessageIds: MutableSet<UUID> = mutableSetOf()
    private val effects: MutableList<CalculationPerformedV1> = mutableListOf()

    @Synchronized
    override fun consume(message: OutboxMessage) {
        TODO("Implement stage")
    }

    @Synchronized
    fun effects(): List<CalculationPerformedV1> = TODO("Implement stage")
}
