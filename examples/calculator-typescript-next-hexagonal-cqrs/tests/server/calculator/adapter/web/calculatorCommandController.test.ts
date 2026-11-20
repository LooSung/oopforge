import { expect, it } from 'vitest';

import { POST as calculate } from '../../../../../src/app/api/v1/calculations/route';

function postCalculation(body: string): Promise<Response> {
  return calculate(
    new Request('http://localhost/api/v1/calculations', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body,
    }),
  );
}

it('returnsOnlyTheId', async () => {
  const response = await postCalculation('{"operandA": 8, "operator": "DIVIDE", "operandB": 2}');

  expect(response.status).toBe(201);
  expect(Object.keys(await response.json())).toEqual(['calculationId']);
});

it('rejectsMalformedJsonWithBadRequest', async () => {
  const response = await postCalculation('{"operandA": 8,');

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
