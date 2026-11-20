package com.oopforge.example.calculator.application.required

import java.time.Instant
import java.util.UUID

data class OutboxMessage(
    val id: UUID,
    val aggregateId: String,
    val eventType: String,
    val payload: Any,
    val occurredAt: Instant,
)
