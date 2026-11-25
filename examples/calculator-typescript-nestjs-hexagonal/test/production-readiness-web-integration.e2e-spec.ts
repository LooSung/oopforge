import type { INestApplication } from '@nestjs/common';
import type { Response } from 'supertest';

import { InMemoryAuditAdapter } from '../src/calculator/adapter/audit/in-memory-audit.adapter.js';
import { CORRELATION_HEADER } from '../src/calculator/adapter/web/correlation-audit.middleware.js';
import { OutboxPort } from '../src/calculator/application/required/outbox.port.js';
import { postCalculation, startApp } from './app.js';

const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

let app: INestApplication;

beforeAll(async () => {
  app = await startApp();
});

afterAll(async () => {
  await app.close();
});

it('rejectsInvalidInputWithSafeJson', async () => {
  const response = await postCalculation(app, '{"operandA":1,"operandB":2}');

  expect(response.status).toBe(400);
  expect(response.headers[CORRELATION_HEADER.toLowerCase()]).toBeDefined();
  expect(JSON.parse(response.text)).toEqual({ code: 'invalid_request', message: 'The request is invalid.' });
  expect(response.text).not.toMatch(/ZodError|operator/);
});

it('rejectsMalformedJsonWithSafeJson', async () => {
  const response = await postCalculation(app, '{"operandA": 6,');

  expect(response.status).toBe(400);
  expect(response.headers[CORRELATION_HEADER.toLowerCase()]).toBeDefined();
  expect(JSON.parse(response.text)).toEqual({ code: 'invalid_request', message: 'The request is invalid.' });
});

it('replaysTheExactFirstResultWithoutAnotherOutboxRow', async () => {
  const initialOutboxRows = await outboxRows();
  const key = crypto.randomUUID();
  const firstBody = '{"operandA":6,"operator":"DIVIDE","operandB":2}';
  const normalizedSameBody = '{"operandB":2.0,"operator":"DIVIDE","operandA":6.0}';

  const first = await performCreated(key, firstBody);
  const duplicate = await performCreated(key, normalizedSameBody);

  expect(duplicate.text).toBe(first.text);
  expect(await outboxRows()).toBe(initialOutboxRows + 1);
});

it('rejectsAnIdempotencyKeyReusedForDifferentInput', async () => {
  const initialOutboxRows = await outboxRows();
  const key = crypto.randomUUID();
  await performCreated(key, '{"operandA":4,"operator":"ADD","operandB":2}');

  const response = await postCalculation(
    app,
    '{"operandA":4,"operator":"MULTIPLY","operandB":2}',
    { 'Idempotency-Key': key },
  );

  expect(response.status).toBe(409);
  expect(response.body).toEqual({
    code: 'idempotency_conflict',
    message: 'The idempotency key was already used for a different request.',
  });
  expect(await outboxRows()).toBe(initialOutboxRows + 1);
});

it('returnsASafeDomainErrorForDivisionByZero', async () => {
  const initialOutboxRows = await outboxRows();

  const response = await postCalculation(app, '{"operandA":1,"operator":"DIVIDE","operandB":0}');

  expect(response.status).toBe(422);
  expect(JSON.parse(response.text)).toEqual({
    code: 'calculation_rejected',
    message: 'The calculation could not be performed.',
  });
  expect(response.text).not.toMatch(/division by zero|DomainRuleViolation/);
  expect(await outboxRows()).toBe(initialOutboxRows);
});

it('generatesAndEchoesACorrelationId', async () => {
  const response = await postCalculation(app, VALID_BODY);

  expect(response.status).toBe(201);
  expect(response.headers[CORRELATION_HEADER.toLowerCase()]).toMatch(UUID);
});

it('echoesAProvidedCorrelationId', async () => {
  const correlationId = 'client-request-123';

  const response = await postCalculation(app, VALID_BODY, { [CORRELATION_HEADER]: correlationId });

  expect(response.status).toBe(201);
  expect(response.headers[CORRELATION_HEADER.toLowerCase()]).toBe(correlationId);
});

it('auditContainsOnlySafeFields', async () => {
  const correlationId = `safe-audit-${crypto.randomUUID()}`;

  const response = await postCalculation(
    app,
    '{"operandA":2,"operator":"ADD","operandB":3,"secret":"body-secret"}',
    {
      [CORRELATION_HEADER]: correlationId,
      Authorization: 'Bearer authorization-secret',
      'X-API-Key': 'api-key-secret',
    },
  );

  expect(response.status).toBe(201);
  const entry = app.get(InMemoryAuditAdapter).entries()
    .find((candidate) => candidate.correlationId === correlationId);
  expect(entry).toMatchObject({ action: 'calculation.create', outcome: 'created' });
  expect(JSON.stringify(entry)).not.toMatch(/authorization-secret|api-key-secret|body-secret/);
  expect(Object.keys(entry ?? {})).toEqual(['correlationId', 'action', 'outcome']);
});

// TypeScript addition: Java's suite never races two same-key requests, but here
// check-then-act spans an await, so the per-key lock needs its own proof.
it('serializesConcurrentRequestsWithTheSameKey', async () => {
  const initialOutboxRows = await outboxRows();
  const key = crypto.randomUUID();
  const body = '{"operandA":9,"operator":"SUBTRACT","operandB":4}';

  const [first, second] = await Promise.all([performCreated(key, body), performCreated(key, body)]);

  expect(second.text).toBe(first.text);
  expect(await outboxRows()).toBe(initialOutboxRows + 1);
});

const VALID_BODY = '{"operandA":2,"operator":"ADD","operandB":3}';

async function performCreated(key: string, body: string): Promise<Response> {
  const response = await postCalculation(app, body, { 'Idempotency-Key': key });
  expect(response.status).toBe(201);
  return response;
}

async function outboxRows(): Promise<number> {
  return (await app.get(OutboxPort).unpublished()).length;
}
