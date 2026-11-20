package com.oopforge.example.calculator.config

import com.oopforge.example.calculator.adapter.messaging.CalculationPerformedConsumer
import com.oopforge.example.calculator.adapter.messaging.OutboxRelay
import com.oopforge.example.calculator.adapter.persistence.InMemoryTransactionalAdapter
import com.oopforge.example.calculator.application.provided.Calculate
import com.oopforge.example.calculator.application.required.CalculationRepository
import com.oopforge.example.calculator.application.required.DomainEventDispatcher
import com.oopforge.example.calculator.application.required.OutboxPort
import com.oopforge.example.calculator.application.required.TransactionRunner
import com.oopforge.example.calculator.application.service.CalculateService
import com.oopforge.example.calculator.application.service.CalculationPerformedHandler
import com.oopforge.example.calculator.application.service.SynchronousDomainEventDispatcher
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration

@Configuration
class CalculatorConfig {

    @Bean
    fun transactionalAdapter(): InMemoryTransactionalAdapter = InMemoryTransactionalAdapter()

    @Bean
    fun calculationPerformedHandler(outbox: OutboxPort): CalculationPerformedHandler =
        CalculationPerformedHandler(outbox)

    @Bean
    fun domainEventDispatcher(handler: CalculationPerformedHandler): DomainEventDispatcher =
        SynchronousDomainEventDispatcher(listOf(handler))

    @Bean
    fun calculate(
        calculationRepository: CalculationRepository,
        transactionRunner: TransactionRunner,
        eventDispatcher: DomainEventDispatcher,
    ): Calculate = CalculateService(calculationRepository, transactionRunner, eventDispatcher)

    @Bean
    fun calculationPerformedConsumer(): CalculationPerformedConsumer = CalculationPerformedConsumer()

    @Bean
    fun outboxRelay(outbox: OutboxPort, consumer: CalculationPerformedConsumer): OutboxRelay =
        OutboxRelay(outbox, consumer)
}
