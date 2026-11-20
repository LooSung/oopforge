package com.oopforge.example.calculator.adapter.messaging

import com.oopforge.example.calculator.application.required.OutboxPort

class OutboxRelay(
    private val outbox: OutboxPort,
    private val consumer: OutboxConsumer,
) {

    fun relay() {
        TODO("Implement stage")
    }
}
