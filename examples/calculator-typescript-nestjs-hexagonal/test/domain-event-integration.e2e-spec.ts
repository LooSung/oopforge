import type { INestApplication } from '@nestjs/common';

import { CalculationPerformedConsumer } from '../src/calculator/adapter/messaging/calculation-performed.consumer.js';
import { OutboxRelay } from '../src/calculator/adapter/messaging/outbox-relay.js';
import { CalculationPerformedV1 } from '../src/calculator/application/integration/calculation-performed-v1.js';
import { OutboxPort } from '../src/calculator/application/required/outbox.port.js';
import { postCalculation, startApp } from './app.js';

let app: INestApplication;

beforeAll(async () => {
  app = await startApp();
});

afterAll(async () => {
  await app.close();
});

it('relaysVersionOnePayloadAndDeduplicatesDuplicateDelivery', async () => {
  const outbox = app.get(OutboxPort);
  const consumer = app.get(CalculationPerformedConsumer);
  await performCalculation();

  const [message] = await outbox.unpublished();
  expect(message.payload).toBeInstanceOf(CalculationPerformedV1);
  const payload = message.payload as CalculationPerformedV1;
  expect(payload.schemaVersion).toBe(1);
  expect(payload.result).toBe(32);

  await app.get(OutboxRelay).relay();
  await consumer.consume(message);

  expect(consumer.effects()).toEqual([payload]);
  expect(await outbox.publishedAt(message.id)).toBeInstanceOf(Date);
});

async function performCalculation(): Promise<void> {
  const response = await postCalculation(app, '{"operandA":8,"operator":"MULTIPLY","operandB":4}');

  expect(response.status).toBe(201);
  expect(response.body).toMatchObject({ operator: 'multiply', result: 32 });
}
