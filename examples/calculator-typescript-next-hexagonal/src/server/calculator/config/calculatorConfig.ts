import 'server-only';
import { CalculationPerformedConsumer } from '../adapter/messaging/calculationPerformedConsumer';
import { OutboxRelay } from '../adapter/messaging/outboxRelay';
import { InMemoryAuditAdapter } from '../adapter/audit/inMemoryAuditAdapter';
import { InMemoryTransactionalAdapter } from '../adapter/persistence/inMemoryTransactionalAdapter';
import { IdempotencyStore } from '../adapter/web/idempotencyStore';
import { IdempotentCalculationHandler } from '../adapter/web/idempotentCalculationHandler';
import type { Calculate } from '../application/provided/calculate';
import type { OutboxPort } from '../application/required/outboxPort';
import { CalculateService } from '../application/service/calculateService';
import { CalculationPerformedHandler } from '../application/service/calculationPerformedHandler';
import { SynchronousDomainEventDispatcher } from '../application/service/synchronousDomainEventDispatcher';

export interface CalculatorConfig {
  readonly calculate: Calculate;
  readonly outbox: OutboxPort;
  readonly relay: OutboxRelay;
  readonly consumer: CalculationPerformedConsumer;
  readonly audit: InMemoryAuditAdapter;
  readonly calculationHandler: IdempotentCalculationHandler;
}

// Replacing one collaborator is how tests stand in for Spring's @MockitoBean.
export interface CalculatorConfigOverrides {
  readonly calculate?: Calculate;
}

// The composition root: Next.js has no DI container, so this wires the graph.
export function createCalculatorConfig(overrides: CalculatorConfigOverrides = {}): CalculatorConfig {
  const store = new InMemoryTransactionalAdapter();
  const dispatcher = new SynchronousDomainEventDispatcher([new CalculationPerformedHandler(store)]);
  const calculate = overrides.calculate ?? new CalculateService(store, store, dispatcher);
  const consumer = new CalculationPerformedConsumer();
  return {
    calculate,
    outbox: store,
    relay: new OutboxRelay(store, consumer),
    consumer,
    audit: new InMemoryAuditAdapter(),
    calculationHandler: new IdempotentCalculationHandler(calculate, new IdempotencyStore()),
  };
}

let defaultConfig: CalculatorConfig | undefined;

// The graph the entry modules use. It is deliberately module-level, not kept
// on globalThis: a graph that outlives a module re-evaluation (a dev reload,
// for example) runs old code and throws error classes the reloaded web
// adapter's instanceof checks no longer recognise. Each evaluation therefore
// starts with empty in-memory stores; durable adapters keep state elsewhere.
export function calculatorConfig(): CalculatorConfig {
  defaultConfig ??= createCalculatorConfig();
  return defaultConfig;
}
