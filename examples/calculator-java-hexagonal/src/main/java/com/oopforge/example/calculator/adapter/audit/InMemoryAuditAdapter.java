package com.oopforge.example.calculator.adapter.audit;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;

@Component
public final class InMemoryAuditAdapter {

    private static final Logger LOGGER = LoggerFactory.getLogger(InMemoryAuditAdapter.class);

    private final List<AuditEntry> entries = new CopyOnWriteArrayList<>();

    public void record(String correlationId, String action, String outcome) {
        AuditEntry entry = new AuditEntry(correlationId, action, outcome);
        entries.add(entry);
        LOGGER.info(
                "audit correlationId={} action={} outcome={}",
                entry.correlationId(),
                entry.action(),
                entry.outcome());
    }

    public List<AuditEntry> entries() {
        return List.copyOf(entries);
    }

    public record AuditEntry(String correlationId, String action, String outcome) {}
}
