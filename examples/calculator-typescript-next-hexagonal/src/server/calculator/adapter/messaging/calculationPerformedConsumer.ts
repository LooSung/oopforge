import { CalculationPerformedV1 } from '../../application/integration/calculationPerformedV1';
import type { OutboxMessage } from '../../application/required/outboxMessage';
import type { OutboxConsumer } from './outboxConsumer';

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
