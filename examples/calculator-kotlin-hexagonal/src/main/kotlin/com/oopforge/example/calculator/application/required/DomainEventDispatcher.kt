package com.oopforge.example.calculator.application.required

import com.oopforge.example.calculator.domain.DomainEvent

interface DomainEventDispatcher {

    fun dispatch(events: List<DomainEvent>)
}
