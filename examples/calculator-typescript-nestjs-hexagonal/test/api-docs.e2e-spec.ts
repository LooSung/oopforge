import type { INestApplication } from '@nestjs/common';
import request from 'supertest';

import { CORRELATION_HEADER } from '../src/calculator/adapter/web/correlation-audit.middleware.js';
import { startApp } from './app.js';

let app: INestApplication;

beforeAll(async () => {
  app = await startApp();
});

afterAll(async () => {
  await app.close();
});

// TypeScript addition: the Java hexagonal reference ships no springdoc, so this
// pins the generated contract to the one HTTP route.
it('documentsTheCalculationRouteOnly', async () => {
  const response = await request(app.getHttpServer()).get('/v3/api-docs');
  const document = response.body;

  expect(response.status).toBe(200);
  expect(response.headers[CORRELATION_HEADER.toLowerCase()]).toBeDefined();
  expect(Object.keys(document.paths)).toEqual(['/calculations']);
  expect(Object.keys(document.paths['/calculations'])).toEqual(['post']);
  expect(Object.keys(document.paths['/calculations'].post.responses))
    .toEqual(['201', '400', '409', '422', '500']);
  expect(Object.keys(document.components.schemas).sort())
    .toEqual(['ApiError', 'CalculateRequest', 'CalculationResponse']);
});
