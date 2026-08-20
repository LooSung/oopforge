package com.oopforge.example.calculator.adapter.persistence;

import com.oopforge.example.calculator.application.required.CalculationRepository;
import com.oopforge.example.calculator.application.required.OutboxMessage;
import com.oopforge.example.calculator.application.required.OutboxPort;
import com.oopforge.example.calculator.application.required.TransactionRunner;
import com.oopforge.example.calculator.domain.Calculation;
import com.oopforge.example.calculator.domain.CalculationId;

import java.time.Instant;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import java.util.function.Supplier;

public final class InMemoryTransactionalAdapter
        implements CalculationRepository, OutboxPort, TransactionRunner {

    private final Map<CalculationId, Calculation> calculations = new ConcurrentHashMap<>();
    private final Map<UUID, OutboxRow> outbox = new LinkedHashMap<>();
    private final ThreadLocal<TransactionState> transactions = new ThreadLocal<>();

    @Override
    public <T> T run(Supplier<T> work) {
        if (transactions.get() != null) {
            throw new IllegalStateException("nested transactions are not supported");
        }
        TransactionState transaction = new TransactionState();
        transactions.set(transaction);
        try {
            T result = work.get();
            commit(transaction);
            return result;
        } finally {
            transactions.remove();
        }
    }

    @Override
    public void save(Calculation calculation) {
        activeTransaction().calculations.put(calculation.id(), calculation);
    }

    @Override
    public Optional<Calculation> findById(CalculationId id) {
        TransactionState transaction = transactions.get();
        if (transaction != null && transaction.calculations.containsKey(id)) {
            return Optional.of(transaction.calculations.get(id));
        }
        return Optional.ofNullable(calculations.get(id));
    }

    @Override
    public void append(OutboxMessage message) {
        activeTransaction().messages.add(message);
    }

    @Override
    public synchronized List<OutboxMessage> unpublished() {
        return outbox.values().stream()
                .filter(row -> row.publishedAt() == null)
                .map(OutboxRow::message)
                .toList();
    }

    @Override
    public synchronized void markPublished(UUID messageId, Instant publishedAt) {
        OutboxRow row = outbox.get(messageId);
        if (row == null) {
            throw new IllegalArgumentException("unknown outbox message");
        }
        outbox.put(messageId, new OutboxRow(row.message(), publishedAt));
    }

    @Override
    public synchronized Optional<Instant> publishedAt(UUID messageId) {
        OutboxRow row = outbox.get(messageId);
        return row == null ? Optional.empty() : Optional.ofNullable(row.publishedAt());
    }

    private TransactionState activeTransaction() {
        TransactionState transaction = transactions.get();
        if (transaction == null) {
            throw new IllegalStateException("operation requires an active transaction");
        }
        return transaction;
    }

    private synchronized void commit(TransactionState transaction) {
        calculations.putAll(transaction.calculations);
        transaction.messages.forEach(message ->
                outbox.put(message.id(), new OutboxRow(message, null)));
    }

    private record OutboxRow(OutboxMessage message, Instant publishedAt) {}

    private static final class TransactionState {
        private final Map<CalculationId, Calculation> calculations = new LinkedHashMap<>();
        private final List<OutboxMessage> messages = new ArrayList<>();
    }
}
