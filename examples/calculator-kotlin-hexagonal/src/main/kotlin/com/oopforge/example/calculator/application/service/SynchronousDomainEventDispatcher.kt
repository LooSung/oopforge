package com.oopforge.example.calculator.application.service

import com.oopforge.example.calculator.application.required.DomainEventDispatcher
import com.oopforge.example.calculator.domain.DomainEvent

class SynchronousDomainEventDispatcher(handlers: List<DomainEventHandler<*>>) : DomainEventDispatcher {

    private val handlers: List<DomainEventHandler<*>> = handlers.toList()

    override fun dispatch(events: List<DomainEvent>) {
        events.forEach { dispatch(it) }
    }

    private fun dispatch(event: DomainEvent) {
        handlers
            .filter { it.eventType().isInstance(event) }
            .forEach { it.handleEvent(event) }
    }
}
