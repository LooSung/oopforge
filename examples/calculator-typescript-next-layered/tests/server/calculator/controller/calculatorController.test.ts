import { expect, it } from 'vitest';

import { POST } from '../../../../src/app/api/v1/calculations/route';

function postCalculation(body: string): Promise<Response> {
  return POST(
    new Request('http://localhost/api/v1/calculations', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body,
    }),
  );
}

it('createsCalculationWithLowerCaseOperator', async () => {
  const response = await postCalculation('{"operandA": 6, "operator": "MULTIPLY", "operandB": 7}');

  expect(response.status).toBe(201);
  expect(await response.json()).toMatchObject({ operandA: 6, operator: 'multiply', operandB: 7, result: 42 });
});

it('rejectsMalformedJsonWithBadRequest', async () => {
  const response = await postCalculation('{"operandA": 6,');

  expect(response.status).toBe(400);
  expect(await response.json()).toEqual({
    status: 400,
    error: 'Bad Request',
    message: 'Malformed JSON request body',
    path: '/api/v1/calculations',
  });
});

it('rejectsMissingOperandWithBadRequest', async () => {
  const response = await postCalculation('{"operator": "ADD", "operandB": 3}');

  expect(response.status).toBe(400);
});

it('rejectsUnknownOperatorWithBadRequest', async () => {
  const response = await postCalculation('{"operandA": 1, "operator": "POWER", "operandB": 3}');

  expect(response.status).toBe(400);
});
