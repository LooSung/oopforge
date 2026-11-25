import { Injectable } from '@nestjs/common';

import { CalculationPerformed } from '../../domain/calculation-performed.js';
import { CalculationPerformedV1 } from '../integration/calculation-performed-v1.js';
import { outboxMessage } from '../required/outbox-message.js';
import { OutboxPort } from '../required/outbox.port.js';
import type { DomainEventHandler } from './domain-event-handler.js';

@Injectable()
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
