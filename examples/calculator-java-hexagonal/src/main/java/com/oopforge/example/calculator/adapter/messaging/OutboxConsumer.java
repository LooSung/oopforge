package com.oopforge.example.calculator.adapter.messaging;

import com.oopforge.example.calculator.application.required.OutboxMessage;

@FunctionalInterface
public interface OutboxConsumer {

    void consume(OutboxMessage message);
}
