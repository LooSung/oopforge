import { expect, it } from 'vitest';
import { createCalculatorController } from '../../../src/server/calculator/adapter/web/calculatorController';
import { CalculationPerformedV1 } from '../../../src/server/calculator/application/integration/calculationPerformedV1';
import { createCalculatorConfig } from '../../../src/server/calculator/config/calculatorConfig';
import { calculationRequest } from '../../support/calculationRequests';

// A fresh graph per file plays the role of the Java test's Spring context.
const config = createCalculatorConfig();
const POST = createCalculatorController(config);

it('relaysVersionOnePayloadAndDeduplicatesDuplicateDelivery', async () => {
  await performCalculation();

  const [message] = await config.outbox.unpublished();
  expect(message.payload).toBeInstanceOf(CalculationPerformedV1);
  const payload = message.payload as CalculationPerformedV1;
  expect(payload.schemaVersion).toBe(1);
  expect(payload.result).toBe(32);

  await config.relay.relay();
  await config.consumer.consume(message);

  expect(config.consumer.effects()).toEqual([payload]);
  expect(await config.outbox.publishedAt(message.id)).toBeInstanceOf(Date);
});

async function performCalculation(): Promise<void> {
  const response = await POST(calculationRequest('{"operandA":8,"operator":"MULTIPLY","operandB":4}'));

  expect(response.status).toBe(201);
  expect(await response.json()).toMatchObject({ operator: 'multiply', result: 32 });
}
