package com.oopforge.example.calculator.application.service;

import com.oopforge.example.calculator.application.required.DomainEventDispatcher;
import com.oopforge.example.calculator.domain.DomainEvent;

import java.util.List;

public final class SynchronousDomainEventDispatcher implements DomainEventDispatcher {

    private final List<DomainEventHandler<?>> handlers;

    public SynchronousDomainEventDispatcher(List<DomainEventHandler<?>> handlers) {
        this.handlers = List.copyOf(handlers);
    }

    @Override
    public void dispatch(List<DomainEvent> events) {
        events.forEach(this::dispatch);
    }

    private void dispatch(DomainEvent event) {
        handlers.stream()
                .filter(handler -> handler.eventType().isInstance(event))
                .forEach(handler -> handler.handleEvent(event));
    }
}
