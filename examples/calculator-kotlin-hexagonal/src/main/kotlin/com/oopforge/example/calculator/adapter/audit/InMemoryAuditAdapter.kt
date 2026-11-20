package com.oopforge.example.calculator.adapter.audit

import org.slf4j.Logger
import org.slf4j.LoggerFactory
import org.springframework.stereotype.Component
import java.util.concurrent.CopyOnWriteArrayList

@Component
class InMemoryAuditAdapter {

    private val entries = CopyOnWriteArrayList<AuditEntry>()

    fun record(correlationId: String, action: String, outcome: String) {
        TODO("Implement stage")
    }

    fun entries(): List<AuditEntry> = TODO("Implement stage")

    data class AuditEntry(val correlationId: String, val action: String, val outcome: String)

    private companion object {
        val LOGGER: Logger = LoggerFactory.getLogger(InMemoryAuditAdapter::class.java)
    }
}
