package com.oopforge.example.calculator.adapter.persistence

import com.oopforge.example.calculator.application.required.CalculationRepository
import com.oopforge.example.calculator.application.required.OutboxMessage
import com.oopforge.example.calculator.application.required.OutboxPort
import com.oopforge.example.calculator.application.required.TransactionRunner
import com.oopforge.example.calculator.domain.Calculation
import com.oopforge.example.calculator.domain.CalculationId
import java.time.Instant
import java.util.UUID
import java.util.concurrent.ConcurrentHashMap

class InMemoryTransactionalAdapter : CalculationRepository, OutboxPort, TransactionRunner {

    private val calculations = ConcurrentHashMap<CalculationId, Calculation>()
    private val outbox = LinkedHashMap<UUID, OutboxRow>()
    private val transactions = ThreadLocal<TransactionState>()

    override fun <T> run(work: () -> T): T = TODO("Implement stage")

    override fun save(calculation: Calculation) {
        TODO("Implement stage")
    }

    override fun findById(id: CalculationId): Calculation? = TODO("Implement stage")

    override fun append(message: OutboxMessage) {
        TODO("Implement stage")
    }

    @Synchronized
    override fun unpublished(): List<OutboxMessage> = TODO("Implement stage")

    @Synchronized
    override fun markPublished(messageId: UUID, publishedAt: Instant) {
        TODO("Implement stage")
    }

    @Synchronized
    override fun publishedAt(messageId: UUID): Instant? = TODO("Implement stage")

    private data class OutboxRow(val message: OutboxMessage, val publishedAt: Instant?)

    private class TransactionState {
        val calculations = LinkedHashMap<CalculationId, Calculation>()
        val messages: MutableList<OutboxMessage> = mutableListOf()
    }
}
