import type { INestApplication } from '@nestjs/common';

import { CORRELATION_HEADER } from '../src/calculator/adapter/web/correlation-audit.middleware.js';
import { Calculate } from '../src/calculator/application/provided/calculate.js';
import { postCalculation, startApp } from './app.js';

let app: INestApplication;

beforeAll(async () => {
  const failing: Pick<Calculate, 'handle'> = {
    handle: () => Promise.reject(new Error('forced internal detail')),
  };
  app = await startApp((builder) => builder.overrideProvider(Calculate).useValue(failing));
});

afterAll(async () => {
  await app.close();
});

it('hidesUnexpectedFailureDetails', async () => {
  const response = await postCalculation(app, '{"operandA":2,"operator":"ADD","operandB":3}');

  expect(response.status).toBe(500);
  expect(response.headers[CORRELATION_HEADER.toLowerCase()]).toBeDefined();
  expect(JSON.parse(response.text)).toEqual({
    code: 'internal_error',
    message: 'The request could not be completed.',
  });
  expect(response.text).not.toMatch(/forced internal detail|Error|Calculate/);
});
