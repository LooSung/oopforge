import { expect, it } from 'vitest';
import { OutboxRelay } from '../../../../../src/server/calculator/adapter/messaging/outboxRelay';
import { InMemoryTransactionalAdapter } from '../../../../../src/server/calculator/adapter/persistence/inMemoryTransactionalAdapter';
import { CalculationPerformedV1 } from '../../../../../src/server/calculator/application/integration/calculationPerformedV1';
import type { OutboxMessage } from '../../../../../src/server/calculator/application/required/outboxMessage';
import { outboxMessage } from '../../../../../src/server/calculator/application/required/outboxMessage';

it('leavesMessageUnpublishedWhenConsumerFails', async () => {
  const store = new InMemoryTransactionalAdapter();
  const message = messageFixture();
  await store.run(() => store.append(message));
  const relay = new OutboxRelay(store, {
    consume: () => Promise.reject(new Error('consumer failed')),
  });

  await expect(relay.relay()).rejects.toThrow('consumer failed');

  expect(await store.unpublished()).toEqual([message]);
  expect(await store.publishedAt(message.id)).toBeUndefined();
});

function messageFixture(): OutboxMessage {
  const occurredAt = '2026-08-20T00:00:00.000Z';
  const payload = CalculationPerformedV1.of({
    schemaVersion: 1,
    calculationId: crypto.randomUUID(),
    result: 4,
    occurredAt,
  });
  return outboxMessage({
    id: crypto.randomUUID(),
    aggregateId: payload.calculationId,
    eventType: CalculationPerformedV1.EVENT_TYPE,
    payload,
    occurredAt,
  });
}
