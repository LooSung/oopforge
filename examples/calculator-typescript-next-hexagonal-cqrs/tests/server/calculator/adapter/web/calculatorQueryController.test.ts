import { expect, it } from 'vitest';

import { GET as getCalculation } from '../../../../../src/app/api/v1/calculations/[calculationId]/route';
import { GET as listHistory } from '../../../../../src/app/api/v1/calculations/history/route';
import { POST as calculate } from '../../../../../src/app/api/v1/calculations/route';

const BASE = 'http://localhost/api/v1/calculations';

function findCalculation(calculationId: string): Promise<Response> {
  return getCalculation(new Request(`${BASE}/${calculationId}`), { params: Promise.resolve({ calculationId }) });
}

async function createCalculation(): Promise<string> {
  const body = JSON.stringify({ operandA: 6, operator: 'MULTIPLY', operandB: 7 });
  const created = await calculate(new Request(BASE, { method: 'POST', body }));
  return (await created.json()).calculationId;
}

it('findsCalculationById', async () => {
  const calculationId = await createCalculation();

  const response = await findCalculation(calculationId);

  expect(response.status).toBe(200);
  expect(await response.json()).toMatchObject({ calculationId, operandA: 6, operandB: 7, operator: 'multiply', result: 42 });
});

it('returnsNotFoundForUnknownId', async () => {
  const response = await findCalculation('7f9c1a52-3b9e-4d8a-9c2f-1e5b6d7a8c90');

  expect(response.status).toBe(404);
});

it('rejectsMalformedIdWithBadRequest', async () => {
  const response = await findCalculation('not-a-uuid');

  expect(response.status).toBe(400);
});

it('rejectsNonPositiveLimitWithBadRequest', async () => {
  const response = listHistory(new Request(`${BASE}/history?limit=0`));

  expect(response.status).toBe(400);
});
