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

it('openApiDocsAvailable', async () => {
  const response = await request(app.getHttpServer()).get('/v3/api-docs');

  expect(response.status).toBe(200);
  expect(response.body.openapi).toBeDefined();
  expect(Object.keys(response.body.paths).sort()).toEqual([
    '/api/v1/calculations',
    '/api/v1/calculations/history',
    '/api/v1/calculations/{calculationId}',
  ]);
  expect(response.body.paths['/api/v1/calculations/history'].get.parameters).toMatchObject([
    { name: 'limit', in: 'query', required: false },
  ]);
});
