import { OpenAPIRegistry, OpenApiGeneratorV3 } from '@asteasolutions/zod-to-openapi';
import type { z } from 'zod';

import { CalculateRequest } from './calculateRequest';
import { CalculationCreatedResponse } from './calculationCreatedResponse';
import { CalculationPathParams } from './calculationPathParams';
import { HistoryEntryResponse } from './historyEntryResponse';
import { HistoryListResponse } from './historyListResponse';
import { HistoryQueryParams } from './historyQueryParams';

type OpenApiDocument = ReturnType<OpenApiGeneratorV3['generateDocument']>;

const BAD_REQUEST = { description: 'Malformed JSON or input that fails validation' };

export function GET(): Response {
  return Response.json(buildOpenApiDocument());
}

function buildOpenApiDocument(): OpenApiDocument {
  const registry = new OpenAPIRegistry();
  registerCalculate(registry);
  registerListHistory(registry);
  registerGetCalculation(registry);
  return new OpenApiGeneratorV3(registry.definitions).generateDocument({
    openapi: '3.0.1',
    info: { title: 'Calculator (hexagonal + CQRS)', version: '0.1.0' },
  });
}

function json(schema: z.ZodType): { 'application/json': { schema: z.ZodType } } {
  return { 'application/json': { schema } };
}

function registerCalculate(registry: OpenAPIRegistry): void {
  registry.registerPath({
    method: 'post',
    path: '/api/v1/calculations',
    tags: ['Calculator Commands'],
    summary: 'Perform a calculation and return its id',
    request: { body: { content: json(CalculateRequest) } },
    responses: { 201: { description: 'Created', content: json(CalculationCreatedResponse) }, 400: BAD_REQUEST },
  });
}

function registerListHistory(registry: OpenAPIRegistry): void {
  registry.registerPath({
    method: 'get',
    path: '/api/v1/calculations/history',
    tags: ['Calculator Queries'],
    summary: 'List recent calculations, most recent first',
    request: { query: HistoryQueryParams },
    responses: { 200: { description: 'OK', content: json(HistoryListResponse) }, 400: BAD_REQUEST },
  });
}

function registerGetCalculation(registry: OpenAPIRegistry): void {
  registry.registerPath({
    method: 'get',
    path: '/api/v1/calculations/{calculationId}',
    tags: ['Calculator Queries'],
    summary: 'Find one calculation in the history',
    request: { params: CalculationPathParams },
    responses: {
      200: { description: 'OK', content: json(HistoryEntryResponse) },
      400: BAD_REQUEST,
      404: { description: 'No calculation with this id' },
    },
  });
}
