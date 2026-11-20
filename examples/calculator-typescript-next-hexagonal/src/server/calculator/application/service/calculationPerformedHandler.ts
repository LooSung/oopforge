import { CalculationPerformed } from '../../domain/calculationPerformed';
import { CalculationPerformedV1 } from '../integration/calculationPerformedV1';
import { outboxMessage } from '../required/outboxMessage';
import type { OutboxPort } from '../required/outboxPort';
import type { DomainEventHandler } from './domainEventHandler';

export class CalculationPerformedHandler implements DomainEventHandler<CalculationPerformed> {
  readonly eventType = CalculationPerformed;

  constructor(private readonly outbox: OutboxPort) {}

  async handle(event: CalculationPerformed): Promise<void> {
    const occurredAt = event.occurredAt.toISOString();
    const payload = CalculationPerformedV1.of({
      schemaVersion: CalculationPerformedV1.SCHEMA_VERSION,
      calculationId: event.calculationId.value,
      result: event.result,
      occurredAt,
    });
    await this.outbox.append(outboxMessage({
      id: event.eventId,
      aggregateId: payload.calculationId,
      eventType: CalculationPerformedV1.EVENT_TYPE,
      payload,
      occurredAt,
    }));
  }
}
