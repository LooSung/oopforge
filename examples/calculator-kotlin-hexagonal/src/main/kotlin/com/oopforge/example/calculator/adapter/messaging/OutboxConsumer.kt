package com.oopforge.example.calculator.adapter.messaging

import com.oopforge.example.calculator.application.required.OutboxMessage

fun interface OutboxConsumer {

    fun consume(message: OutboxMessage)
}
