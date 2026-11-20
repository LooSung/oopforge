package com.oopforge.example.calculator.application.required

import java.time.Instant
import java.util.UUID

interface OutboxPort {

    fun append(message: OutboxMessage)

    fun unpublished(): List<OutboxMessage>

    fun markPublished(messageId: UUID, publishedAt: Instant)

    fun publishedAt(messageId: UUID): Instant?
}
