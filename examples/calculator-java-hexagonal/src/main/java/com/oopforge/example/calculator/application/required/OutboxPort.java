package com.oopforge.example.calculator.application.required;

import java.time.Instant;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

public interface OutboxPort {

    void append(OutboxMessage message);

    List<OutboxMessage> unpublished();

    void markPublished(UUID messageId, Instant publishedAt);

    Optional<Instant> publishedAt(UUID messageId);
}
