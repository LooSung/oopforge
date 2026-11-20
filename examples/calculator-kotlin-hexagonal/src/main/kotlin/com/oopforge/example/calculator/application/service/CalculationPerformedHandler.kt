package com.oopforge.example.calculator.application.service

import com.oopforge.example.calculator.application.integration.CalculationPerformedV1
import com.oopforge.example.calculator.application.required.OutboxMessage
import com.oopforge.example.calculator.application.required.OutboxPort
import com.oopforge.example.calculator.domain.CalculationPerformed

class CalculationPerformedHandler(private val outbox: OutboxPort) : DomainEventHandler<CalculationPerformed> {

    override fun eventType(): Class<CalculationPerformed> = CalculationPerformed::class.java

    override fun handle(event: CalculationPerformed) {
        val payload = CalculationPerformedV1(
            CalculationPerformedV1.SCHEMA_VERSION,
            event.calculationId.value.toString(),
            event.result,
            event.occurredAt,
        )
        outbox.append(
            OutboxMessage(
                event.eventId,
                payload.calculationId,
                CalculationPerformedV1::class.java.simpleName,
                payload,
                event.occurredAt,
            ),
        )
    }
}
