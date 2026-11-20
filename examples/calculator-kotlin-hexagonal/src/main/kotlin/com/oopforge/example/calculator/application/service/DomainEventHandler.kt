package com.oopforge.example.calculator.application.service

import com.oopforge.example.calculator.domain.DomainEvent

interface DomainEventHandler<T : DomainEvent> {

    fun eventType(): Class<T>

    fun handle(event: T)

    fun handleEvent(event: DomainEvent) {
        TODO("Implement stage")
    }
}
