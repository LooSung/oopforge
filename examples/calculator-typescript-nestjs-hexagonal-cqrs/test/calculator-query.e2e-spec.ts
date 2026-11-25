import type { INestApplication } from '@nestjs/common';
import request from 'supertest';

import { startApp } from './app.js';

const BASE = '/api/v1/calculations';

let app: INestApplication;

beforeAll(async () => {
  app = await startApp();
});

afterAll(async () => {
  await app.close();
});

function findCalculation(calculationId: string): request.Test {
  return request(app.getHttpServer()).get(`${BASE}/${calculationId}`);
}

async function createCalculation(): Promise<string> {
  const created = await request(app.getHttpServer()).post(BASE).send({ operandA: 6, operator: 'MULTIPLY', operandB: 7 });
  return created.body.calculationId;
}

it('findsCalculationById', async () => {
  const calculationId = await createCalculation();

  const response = await findCalculation(calculationId);

  expect(response.status).toBe(200);
  expect(response.body).toMatchObject({ calculationId, operandA: 6, operandB: 7, operator: 'multiply', result: 42 });
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
  const response = await request(app.getHttpServer()).get(`${BASE}/history?limit=0`);

  expect(response.status).toBe(400);
});
