import { Module } from '@nestjs/common';

import { InMemoryAuditAdapter } from './adapter/audit/in-memory-audit.adapter.js';
import { CalculationPerformedConsumer } from './adapter/messaging/calculation-performed.consumer.js';
import { OutboxConsumer } from './adapter/messaging/outbox-consumer.js';
import { OutboxRelay } from './adapter/messaging/outbox-relay.js';
import { InMemoryTransactionalAdapter } from './adapter/persistence/in-memory-transactional.adapter.js';
import { CalculatorController } from './adapter/web/calculator.controller.js';
import { IdempotencyStore } from './adapter/web/idempotency.store.js';
import { IdempotentCalculationHandler } from './adapter/web/idempotent-calculation.handler.js';
import { Calculate } from './application/provided/calculate.js';
import { CalculationRepository } from './application/required/calculation.repository.js';
import { DomainEventDispatcher } from './application/required/domain-event-dispatcher.js';
import { OutboxPort } from './application/required/outbox.port.js';
import { TransactionRunner } from './application/required/transaction-runner.js';
import { CalculateService } from './application/service/calculate.service.js';
import { CalculationPerformedHandler } from './application/service/calculation-performed.handler.js';
import { SynchronousDomainEventDispatcher } from './application/service/synchronous-domain-event-dispatcher.js';

// Composition: the only file that binds ports to adapters. One in-memory
// adapter plays repository, outbox, and transaction runner, so a calculation
// and its outbox rows commit together.
@Module({
  controllers: [CalculatorController],
  providers: [
    InMemoryTransactionalAdapter,
    { provide: CalculationRepository, useExisting: InMemoryTransactionalAdapter },
    { provide: OutboxPort, useExisting: InMemoryTransactionalAdapter },
    { provide: TransactionRunner, useExisting: InMemoryTransactionalAdapter },
    CalculationPerformedHandler,
    {
      provide: DomainEventDispatcher,
      useFactory: (handler: CalculationPerformedHandler) => new SynchronousDomainEventDispatcher([handler]),
      inject: [CalculationPerformedHandler],
    },
    { provide: Calculate, useClass: CalculateService },
    CalculationPerformedConsumer,
    { provide: OutboxConsumer, useExisting: CalculationPerformedConsumer },
    OutboxRelay,
    InMemoryAuditAdapter,
    IdempotencyStore,
    IdempotentCalculationHandler,
  ],
})
export class CalculatorModule {}
