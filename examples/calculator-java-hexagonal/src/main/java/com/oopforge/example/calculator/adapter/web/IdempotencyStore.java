package com.oopforge.example.calculator.adapter.web;

import org.springframework.stereotype.Component;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.function.Supplier;

@Component
final class IdempotencyStore {

    private static final int MAX_KEY_LENGTH = 200;

    private final Map<String, StoredResult> results = new ConcurrentHashMap<>();
    private final Map<String, Object> locks = new ConcurrentHashMap<>();

    CalculationResponse execute(
            String key,
            NormalizedRequest request,
            Supplier<CalculationResponse> operation) {
        if (key == null) {
            return operation.get();
        }
        validate(key);
        synchronized (locks.computeIfAbsent(key, ignored -> new Object())) {
            return executeLocked(key, request, operation);
        }
    }

    private CalculationResponse executeLocked(
            String key,
            NormalizedRequest request,
            Supplier<CalculationResponse> operation) {
        StoredResult stored = results.get(key);
        if (stored == null) {
            CalculationResponse response = operation.get();
            results.put(key, new StoredResult(request, response));
            return response;
        }
        if (!stored.request().equals(request)) {
            throw new IdempotencyConflictException();
        }
        return stored.response();
    }

    private void validate(String key) {
        if (key.isBlank() || key.length() > MAX_KEY_LENGTH) {
            throw new InvalidWebRequestException();
        }
    }

    private record StoredResult(NormalizedRequest request, CalculationResponse response) {}
}
