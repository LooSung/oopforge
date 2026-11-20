package com.oopforge.example.calculator.config

import com.oopforge.example.calculator.adapter.messaging.CalculationPerformedConsumer
import com.oopforge.example.calculator.adapter.messaging.OutboxRelay
import com.oopforge.example.calculator.adapter.persistence.InMemoryTransactionalAdapter
import com.oopforge.example.calculator.application.provided.Calculate
import com.oopforge.example.calculator.application.required.CalculationRepository
import com.oopforge.example.calculator.application.required.DomainEventDispatcher
import com.oopforge.example.calculator.application.required.OutboxPort
import com.oopforge.example.calculator.application.required.TransactionRunner
import com.oopforge.example.calculator.application.service.CalculationPerformedHandler
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration

@Configuration
class CalculatorConfig {

    @Bean
    fun transactionalAdapter(): InMemoryTransactionalAdapter = TODO("Implement stage")

    @Bean
    fun calculationPerformedHandler(outbox: OutboxPort): CalculationPerformedHandler = TODO("Implement stage")

    @Bean
    fun domainEventDispatcher(handler: CalculationPerformedHandler): DomainEventDispatcher = TODO("Implement stage")

    @Bean
    fun calculate(
        calculationRepository: CalculationRepository,
        transactionRunner: TransactionRunner,
        eventDispatcher: DomainEventDispatcher,
    ): Calculate = TODO("Implement stage")

    @Bean
    fun calculationPerformedConsumer(): CalculationPerformedConsumer = TODO("Implement stage")

    @Bean
    fun outboxRelay(outbox: OutboxPort, consumer: CalculationPerformedConsumer): OutboxRelay = TODO("Implement stage")
}
