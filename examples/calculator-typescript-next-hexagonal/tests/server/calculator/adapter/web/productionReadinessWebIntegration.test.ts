import { expect, it } from 'vitest';
import { createCalculatorController } from '../../../../../src/server/calculator/adapter/web/calculatorController';
import { CORRELATION_HEADER } from '../../../../../src/server/calculator/adapter/web/correlationAuditFilter';
import { createCalculatorConfig } from '../../../../../src/server/calculator/config/calculatorConfig';
import { calculationRequest } from '../../../../support/calculationRequests';

const config = createCalculatorConfig();
const POST = createCalculatorController(config);

const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

it('rejectsInvalidInputWithSafeJson', async () => {
  const response = await POST(calculationRequest('{"operandA":1,"operandB":2}'));
  const body = await response.text();

  expect(response.status).toBe(400);
  expect(response.headers.has(CORRELATION_HEADER)).toBe(true);
  expect(JSON.parse(body)).toEqual({ code: 'invalid_request', message: 'The request is invalid.' });
  expect(body).not.toMatch(/ZodError|operator/);
});

it('replaysTheExactFirstResultWithoutAnotherOutboxRow', async () => {
  const initialOutboxRows = await outboxRows();
  const key = crypto.randomUUID();
  const firstBody = '{"operandA":6,"operator":"DIVIDE","operandB":2}';
  const normalizedSameBody = '{"operandB":2.0,"operator":"DIVIDE","operandA":6.0}';

  const first = await performCreated(key, firstBody);
  const duplicate = await performCreated(key, normalizedSameBody);

  expect(await duplicate.text()).toBe(await first.text());
  expect(await outboxRows()).toBe(initialOutboxRows + 1);
});

it('rejectsAnIdempotencyKeyReusedForDifferentInput', async () => {
  const initialOutboxRows = await outboxRows();
  const key = crypto.randomUUID();
  await performCreated(key, '{"operandA":4,"operator":"ADD","operandB":2}');

  const response = await POST(calculationRequest(
    '{"operandA":4,"operator":"MULTIPLY","operandB":2}',
    { 'Idempotency-Key': key },
  ));

  expect(response.status).toBe(409);
  expect(await response.json()).toEqual({
    code: 'idempotency_conflict',
    message: 'The idempotency key was already used for a different request.',
  });
  expect(await outboxRows()).toBe(initialOutboxRows + 1);
});

it('returnsASafeDomainErrorForDivisionByZero', async () => {
  const initialOutboxRows = await outboxRows();

  const response = await POST(calculationRequest('{"operandA":1,"operator":"DIVIDE","operandB":0}'));
  const body = await response.text();

  expect(response.status).toBe(422);
  expect(JSON.parse(body)).toEqual({
    code: 'calculation_rejected',
    message: 'The calculation could not be performed.',
  });
  expect(body).not.toMatch(/division by zero|DomainRuleViolation/);
  expect(await outboxRows()).toBe(initialOutboxRows);
});

it('generatesAndEchoesACorrelationId', async () => {
  const response = await POST(validCalculation());

  expect(response.status).toBe(201);
  expect(response.headers.get(CORRELATION_HEADER)).toMatch(UUID);
});

it('echoesAProvidedCorrelationId', async () => {
  const correlationId = 'client-request-123';

  const response = await POST(validCalculation({ [CORRELATION_HEADER]: correlationId }));

  expect(response.status).toBe(201);
  expect(response.headers.get(CORRELATION_HEADER)).toBe(correlationId);
});

it('auditContainsOnlySafeFields', async () => {
  const correlationId = `safe-audit-${crypto.randomUUID()}`;

  const response = await POST(calculationRequest(
    '{"operandA":2,"operator":"ADD","operandB":3,"secret":"body-secret"}',
    {
      [CORRELATION_HEADER]: correlationId,
      Authorization: 'Bearer authorization-secret',
      'X-API-Key': 'api-key-secret',
    },
  ));

  expect(response.status).toBe(201);
  const entry = config.audit.entries().find((candidate) => candidate.correlationId === correlationId);
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

  expect(await second.text()).toBe(await first.text());
  expect(await outboxRows()).toBe(initialOutboxRows + 1);
});

async function performCreated(key: string, body: string): Promise<Response> {
  const response = await POST(calculationRequest(body, { 'Idempotency-Key': key }));
  expect(response.status).toBe(201);
  return response;
}

function validCalculation(headers: Record<string, string> = {}): Request {
  return calculationRequest('{"operandA":2,"operator":"ADD","operandB":3}', headers);
}

async function outboxRows(): Promise<number> {
  return (await config.outbox.unpublished()).length;
}
