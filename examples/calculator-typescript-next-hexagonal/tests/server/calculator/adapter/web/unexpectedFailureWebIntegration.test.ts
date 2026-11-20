import { expect, it } from 'vitest';
import { createCalculatorController } from '../../../../../src/server/calculator/adapter/web/calculatorController';
import { CORRELATION_HEADER } from '../../../../../src/server/calculator/adapter/web/correlationAuditFilter';
import type { Calculate } from '../../../../../src/server/calculator/application/provided/calculate';
import { createCalculatorConfig } from '../../../../../src/server/calculator/config/calculatorConfig';
import { calculationRequest } from '../../../../support/calculationRequests';

it('hidesUnexpectedFailureDetails', async () => {
  // Replacing Calculate in the composition root stands in for @MockitoBean.
  const calculate: Calculate = { handle: () => Promise.reject(new Error('forced internal detail')) };
  const POST = createCalculatorController(createCalculatorConfig({ calculate }));

  const response = await POST(calculationRequest('{"operandA":2,"operator":"ADD","operandB":3}'));
  const body = await response.text();

  expect(response.status).toBe(500);
  expect(response.headers.has(CORRELATION_HEADER)).toBe(true);
  expect(JSON.parse(body)).toEqual({
    code: 'internal_error',
    message: 'The request could not be completed.',
  });
  expect(body).not.toMatch(/forced internal detail|Error|Calculate/);
});
