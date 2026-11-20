package com.oopforge.example.calculator.domain

import java.time.Instant
import java.util.UUID

abstract class DomainEvent protected constructor() {
    val eventId: UUID = UUID.randomUUID()
    val occurredAt: Instant = Instant.now()
}
