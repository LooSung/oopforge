package com.oopforge.example.calculator.config;

import com.oopforge.example.calculator.adapter.messaging.CalculationPerformedConsumer;
import com.oopforge.example.calculator.adapter.messaging.OutboxRelay;
import com.oopforge.example.calculator.adapter.persistence.InMemoryTransactionalAdapter;
import com.oopforge.example.calculator.application.provided.Calculate;
import com.oopforge.example.calculator.application.required.CalculationRepository;
import com.oopforge.example.calculator.application.required.DomainEventDispatcher;
import com.oopforge.example.calculator.application.required.OutboxPort;
import com.oopforge.example.calculator.application.required.TransactionRunner;
import com.oopforge.example.calculator.application.service.CalculationPerformedHandler;
import com.oopforge.example.calculator.application.service.CalculateService;
import com.oopforge.example.calculator.application.service.SynchronousDomainEventDispatcher;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.List;

@Configuration
public class CalculatorConfig {

    @Bean
    InMemoryTransactionalAdapter transactionalAdapter() {
        return new InMemoryTransactionalAdapter();
    }

    @Bean
    CalculationPerformedHandler calculationPerformedHandler(OutboxPort outbox) {
        return new CalculationPerformedHandler(outbox);
    }

    @Bean
    DomainEventDispatcher domainEventDispatcher(CalculationPerformedHandler handler) {
        return new SynchronousDomainEventDispatcher(List.of(handler));
    }

    @Bean
    Calculate calculate(
            CalculationRepository calculationRepository,
            TransactionRunner transactionRunner,
            DomainEventDispatcher eventDispatcher) {
        return new CalculateService(calculationRepository, transactionRunner, eventDispatcher);
    }

    @Bean
    CalculationPerformedConsumer calculationPerformedConsumer() {
        return new CalculationPerformedConsumer();
    }

    @Bean
    OutboxRelay outboxRelay(OutboxPort outbox, CalculationPerformedConsumer consumer) {
        return new OutboxRelay(outbox, consumer);
    }
}
