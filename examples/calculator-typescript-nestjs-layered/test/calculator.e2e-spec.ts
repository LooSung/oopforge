import type { INestApplication } from '@nestjs/common';
import request from 'supertest';

import { startApp } from './app.js';

let app: INestApplication;

beforeAll(async () => {
  app = await startApp();
});

afterAll(async () => {
  await app.close();
});

function postCalculation(body: string): request.Test {
  return request(app.getHttpServer())
    .post('/api/v1/calculations')
    .set('Content-Type', 'application/json')
    .send(body);
}

it('createsCalculationWithLowerCaseOperator', async () => {
  const response = await postCalculation('{"operandA": 6, "operator": "MULTIPLY", "operandB": 7}');

  expect(response.status).toBe(201);
  expect(response.body).toMatchObject({ operandA: 6, operator: 'multiply', operandB: 7, result: 42 });
});

it('rejectsMalformedJsonWithBadRequest', async () => {
  const response = await postCalculation('{"operandA": 6,');

  expect(response.status).toBe(400);
});

it('rejectsMissingOperandWithBadRequest', async () => {
  const response = await postCalculation('{"operator": "ADD", "operandB": 3}');

  expect(response.status).toBe(400);
});

it('rejectsUnknownOperatorWithBadRequest', async () => {
  const response = await postCalculation('{"operandA": 1, "operator": "POWER", "operandB": 3}');

  expect(response.status).toBe(400);
});
