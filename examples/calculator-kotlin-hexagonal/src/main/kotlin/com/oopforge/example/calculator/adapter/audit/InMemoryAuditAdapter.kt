package com.oopforge.example.calculator.adapter.audit

import org.slf4j.Logger
import org.slf4j.LoggerFactory
import org.springframework.stereotype.Component
import java.util.concurrent.CopyOnWriteArrayList

@Component
class InMemoryAuditAdapter {

    private val entries = CopyOnWriteArrayList<AuditEntry>()

    fun record(correlationId: String, action: String, outcome: String) {
        val entry = AuditEntry(correlationId, action, outcome)
        entries.add(entry)
        LOGGER.info(
            "audit correlationId={} action={} outcome={}",
            entry.correlationId,
            entry.action,
            entry.outcome,
        )
    }

    fun entries(): List<AuditEntry> = entries.toList()

    data class AuditEntry(val correlationId: String, val action: String, val outcome: String)

    private companion object {
        val LOGGER: Logger = LoggerFactory.getLogger(InMemoryAuditAdapter::class.java)
    }
}
