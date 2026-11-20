import { expect, it } from 'vitest';

import { GET as listHistory } from '../../../../../src/app/api/v1/calculations/history/route';
import { POST as calculate } from '../../../../../src/app/api/v1/calculations/route';

it('commandCreatesThenQueryReturnsHistory', async () => {
  const created = await calculate(
    new Request('http://localhost/api/v1/calculations', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: '{"operandA":2,"operator":"ADD","operandB":3}',
    }),
  );
  expect(created.status).toBe(201);
  expect((await created.json()).calculationId).toBeDefined();

  const history = await listHistory(new Request('http://localhost/api/v1/calculations/history'));
  const body = await history.json();
  expect(history.status).toBe(200);
  expect(body.items[0].result).toBe(5.0);
  expect(body.items[0].operator).toBe('add');
});
