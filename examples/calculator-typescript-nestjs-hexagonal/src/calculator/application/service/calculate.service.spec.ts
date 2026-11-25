import { InMemoryTransactionalAdapter } from '../../adapter/persistence/in-memory-transactional.adapter.js';
import type { Calculation } from '../../domain/calculation.js';
import { CalculationId } from '../../domain/calculation-id.js';
import { CalculationPerformed } from '../../domain/calculation-performed.js';
import type { DomainEvent } from '../../domain/domain-event.js';
import { Operator } from '../../domain/operator.js';
import type { CalculationRepository } from '../required/calculation.repository.js';
import type { DomainEventDispatcher } from '../required/domain-event-dispatcher.js';
import type { TransactionRunner } from '../required/transaction-runner.js';
import { CalculateService } from './calculate.service.js';
import { CalculationPerformedHandler } from './calculation-performed.handler.js';
import type { DomainEventHandler } from './domain-event-handler.js';
import { SynchronousDomainEventDispatcher } from './synchronous-domain-event-dispatcher.js';

it('savesBeforeDrainingAndDispatchesEventsOnce', async () => {
  const calls: string[] = [];
  const repository = new RecordingRepository(calls);
  const dispatcher = new RecordingDispatcher(calls);
  const service = new CalculateService(repository, new RecordingTransactionRunner(calls), dispatcher);

  await service.handle({ operandA: 2, operator: Operator.ADD, operandB: 3 });

  expect(calls).toEqual(['transaction', 'save', 'dispatch']);
  expect(dispatcher.invocationCount).toBe(1);
  expect(dispatcher.events).toHaveLength(1);
  expect(repository.saved()?.popEvents()).toEqual([]);
});

it('appendsTheDrainedEventToTheOutbox', async () => {
  const store = new InMemoryTransactionalAdapter();
  const dispatcher = dispatcherWith(new CalculationPerformedHandler(store));
  const service = new CalculateService(store, store, dispatcher);

  const result = await service.handle({ operandA: 8, operator: Operator.MULTIPLY, operandB: 4 });

  const saved = await store.findById(CalculationId.of(result.calculationId));
  expect(saved).toBeDefined();
  expect(saved?.popEvents()).toEqual([]);
  expect(await store.unpublished()).toHaveLength(1);
});

it('rollsBackCalculationAndOutboxWhenAHandlerFails', async () => {
  const store = new InMemoryTransactionalAdapter();
  const failingHandler = new FailingHandler();
  const dispatcher = dispatcherWith(new CalculationPerformedHandler(store), failingHandler);
  const service = new CalculateService(store, store, dispatcher);

  await expect(service.handle({ operandA: 8, operator: Operator.DIVIDE, operandB: 2 }))
    .rejects.toThrow('handler failed');

  expect(await store.findById(failingHandler.event().calculationId)).toBeUndefined();
  expect(await store.unpublished()).toEqual([]);
});

function dispatcherWith(...handlers: DomainEventHandler<DomainEvent>[]): DomainEventDispatcher {
  return new SynchronousDomainEventDispatcher(handlers);
}

class RecordingTransactionRunner implements TransactionRunner {
  constructor(private readonly calls: string[]) {}

  async run<T>(work: () => Promise<T>): Promise<T> {
    this.calls.push('transaction');
    return work();
  }
}

class RecordingRepository implements CalculationRepository {
  private savedCalculation: Calculation | undefined;

  constructor(private readonly calls: string[]) {}

  async save(calculation: Calculation): Promise<void> {
    this.calls.push('save');
    this.savedCalculation = calculation;
  }

  async findById(id: CalculationId): Promise<Calculation | undefined> {
    return this.savedCalculation?.id.equals(id) ? this.savedCalculation : undefined;
  }

  saved(): Calculation | undefined {
    return this.savedCalculation;
  }
}

class RecordingDispatcher implements DomainEventDispatcher {
  private dispatched: ReadonlyArray<DomainEvent> = [];
  private invocations = 0;

  constructor(private readonly calls: string[]) {}

  get events(): ReadonlyArray<DomainEvent> {
    return this.dispatched;
  }

  get invocationCount(): number {
    return this.invocations;
  }

  async dispatch(events: ReadonlyArray<DomainEvent>): Promise<void> {
    this.calls.push('dispatch');
    this.dispatched = [...events];
    this.invocations += 1;
  }
}

class FailingHandler implements DomainEventHandler<CalculationPerformed> {
  readonly eventType = CalculationPerformed;
  private handled: CalculationPerformed | undefined;

  async handle(event: CalculationPerformed): Promise<void> {
    this.handled = event;
    throw new Error('handler failed');
  }

  event(): CalculationPerformed {
    if (this.handled === undefined) {
      throw new Error('the handler never ran');
    }
    return this.handled;
  }
}
