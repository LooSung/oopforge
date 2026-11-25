import { Injectable } from '@nestjs/common';

import { CalculationPerformedV1 } from '../../application/integration/calculation-performed-v1.js';
import type { OutboxMessage } from '../../application/required/outbox-message.js';
import type { OutboxConsumer } from './outbox-consumer.js';

@Injectable()
export class CalculationPerformedConsumer implements OutboxConsumer {
  private readonly processedMessageIds = new Set<string>();
  private readonly recordedEffects: CalculationPerformedV1[] = [];

  async consume(message: OutboxMessage): Promise<void> {
    const payload = payloadOf(message);
    if (this.processedMessageIds.has(message.id)) {
      return;
    }
    this.recordedEffects.push(payload);
    this.processedMessageIds.add(message.id);
  }

  effects(): ReadonlyArray<CalculationPerformedV1> {
    return [...this.recordedEffects];
  }
}

function payloadOf(message: OutboxMessage): CalculationPerformedV1 {
  if (message.payload instanceof CalculationPerformedV1) {
    return message.payload;
  }
  throw new TypeError('unsupported outbox payload');
}
