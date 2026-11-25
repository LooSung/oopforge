import type { INestApplication } from '@nestjs/common';
import { Test, type TestingModuleBuilder } from '@nestjs/testing';
import request from 'supertest';

import { AppModule } from '../src/app.module.js';
import { configureApp } from '../src/configure-app.js';

type Customize = (builder: TestingModuleBuilder) => TestingModuleBuilder;

// A fresh application per file plays the role of the Java test's Spring
// context; overrideProvider() stands in for @MockitoBean.
export async function startApp(customize: Customize = (builder) => builder): Promise<INestApplication> {
  const moduleRef = await customize(Test.createTestingModule({ imports: [AppModule] })).compile();
  const app = configureApp(moduleRef.createNestApplication());
  await app.init();
  return app;
}

export function postCalculation(
  app: INestApplication,
  body: string,
  headers: Record<string, string> = {},
): request.Test {
  return request(app.getHttpServer())
    .post('/calculations')
    .set({ 'Content-Type': 'application/json', ...headers })
    .send(body);
}
