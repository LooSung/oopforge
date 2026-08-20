package com.oopforge.example.calculator.application.service;

import com.oopforge.example.calculator.domain.DomainEvent;

public interface DomainEventHandler<T extends DomainEvent> {

    Class<T> eventType();

    void handle(T event);

    default void handleEvent(DomainEvent event) {
        handle(eventType().cast(event));
    }
}
