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

it('commandCreatesThenQueryReturnsHistory', async () => {
  const created = await request(app.getHttpServer())
    .post('/api/v1/calculations')
    .send({ operandA: 2, operator: 'ADD', operandB: 3 });
  expect(created.status).toBe(201);
  expect(created.body.calculationId).toBeDefined();

  const history = await request(app.getHttpServer()).get('/api/v1/calculations/history');
  expect(history.status).toBe(200);
  expect(history.body.items[0].result).toBe(5.0);
  expect(history.body.items[0].operator).toBe('add');
});
