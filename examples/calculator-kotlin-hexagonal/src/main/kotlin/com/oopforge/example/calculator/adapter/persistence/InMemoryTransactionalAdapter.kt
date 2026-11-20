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

    override fun <T> run(work: () -> T): T {
        check(transactions.get() == null) { "nested transactions are not supported" }
        val transaction = TransactionState()
        transactions.set(transaction)
        try {
            val result = work()
            commit(transaction)
            return result
        } finally {
            transactions.remove()
        }
    }

    override fun save(calculation: Calculation) {
        activeTransaction().calculations[calculation.id] = calculation
    }

    override fun findById(id: CalculationId): Calculation? =
        transactions.get()?.calculations?.get(id) ?: calculations[id]

    override fun append(message: OutboxMessage) {
        activeTransaction().messages.add(message)
    }

    @Synchronized
    override fun unpublished(): List<OutboxMessage> =
        outbox.values.filter { it.publishedAt == null }.map { it.message }

    @Synchronized
    override fun markPublished(messageId: UUID, publishedAt: Instant) {
        val row = requireNotNull(outbox[messageId]) { "unknown outbox message" }
        outbox[messageId] = row.copy(publishedAt = publishedAt)
    }

    @Synchronized
    override fun publishedAt(messageId: UUID): Instant? = outbox[messageId]?.publishedAt

    private fun activeTransaction(): TransactionState =
        checkNotNull(transactions.get()) { "operation requires an active transaction" }

    @Synchronized
    private fun commit(transaction: TransactionState) {
        calculations.putAll(transaction.calculations)
        transaction.messages.forEach { outbox[it.id] = OutboxRow(it, null) }
    }

    private data class OutboxRow(val message: OutboxMessage, val publishedAt: Instant?)

    private class TransactionState {
        val calculations = LinkedHashMap<CalculationId, Calculation>()
        val messages: MutableList<OutboxMessage> = mutableListOf()
    }
}
