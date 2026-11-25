import { InMemoryTransactionalAdapter } from '../persistence/in-memory-transactional.adapter.js';
import { CalculationPerformedV1 } from '../../application/integration/calculation-performed-v1.js';
import { outboxMessage, type OutboxMessage } from '../../application/required/outbox-message.js';
import { OutboxRelay } from './outbox-relay.js';

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
