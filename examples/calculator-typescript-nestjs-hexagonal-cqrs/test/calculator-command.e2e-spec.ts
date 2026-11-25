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

it('returnsOnlyTheId', async () => {
  const response = await postCalculation('{"operandA": 8, "operator": "DIVIDE", "operandB": 2}');

  expect(response.status).toBe(201);
  expect(Object.keys(response.body)).toEqual(['calculationId']);
});

it('rejectsMalformedJsonWithBadRequest', async () => {
  const response = await postCalculation('{"operandA": 8,');

  expect(response.status).toBe(400);
});

it('rejectsMissingOperandWithBadRequest', async () => {
  const response = await postCalculation('{"operator": "ADD", "operandB": 3}');

  expect(response.status).toBe(400);
});
