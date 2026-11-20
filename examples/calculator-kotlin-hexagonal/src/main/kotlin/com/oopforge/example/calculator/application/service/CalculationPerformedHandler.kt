package com.oopforge.example.calculator.application.service

import com.oopforge.example.calculator.application.required.OutboxPort
import com.oopforge.example.calculator.domain.CalculationPerformed

class CalculationPerformedHandler(private val outbox: OutboxPort) : DomainEventHandler<CalculationPerformed> {

    override fun eventType(): Class<CalculationPerformed> = TODO("Implement stage")

    override fun handle(event: CalculationPerformed) {
        TODO("Implement stage")
    }
}
