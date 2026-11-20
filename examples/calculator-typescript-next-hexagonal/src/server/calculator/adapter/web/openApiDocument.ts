import type { ResponseConfig } from '@asteasolutions/zod-to-openapi';
import { OpenAPIRegistry, OpenApiGeneratorV3 } from '@asteasolutions/zod-to-openapi';
import { z } from 'zod';
import { apiErrorSchema } from './apiError';
import { calculateRequestSchema } from './calculateRequest';
import { calculationResponseSchema } from './calculationResponse';
import { CORRELATION_HEADER } from './correlationAuditFilter';
import { IDEMPOTENCY_KEY_HEADER, MAX_KEY_LENGTH } from './idempotencyStore';

// Must match the route file location: src/app/calculations/route.ts.
export const CALCULATIONS_PATH = '/calculations';

export type OpenApiDocument = ReturnType<OpenApiGeneratorV3['generateDocument']>;

const correlationHeader = z.object({
  [CORRELATION_HEADER]: z.string().meta({ description: 'Echoed or generated correlation id' }),
});

// Route handlers are the HTTP contract, so they are documented; the server
// action is internal RPC and deliberately left out.
export function buildOpenApiDocument(): OpenApiDocument {
  const registry = new OpenAPIRegistry();
  registry.registerPath({
    method: 'post',
    path: CALCULATIONS_PATH,
    summary: 'Perform a calculation',
    request: {
      headers: z.object({
        [IDEMPOTENCY_KEY_HEADER]: z.string().min(1).max(MAX_KEY_LENGTH).optional(),
        [CORRELATION_HEADER]: z.string().optional(),
      }),
      body: { required: true, content: { 'application/json': { schema: calculateRequestSchema } } },
    },
    responses: calculationResponses(),
  });
  return new OpenApiGeneratorV3(registry.definitions).generateDocument({
    openapi: '3.0.1',
    info: { title: 'Calculator (TypeScript Next.js hexagonal)', version: '0.1.0' },
  });
}

function calculationResponses(): Record<string, ResponseConfig> {
  return {
    201: {
      description: 'Calculation performed, or the stored result replayed for a repeated key',
      headers: correlationHeader,
      content: { 'application/json': { schema: calculationResponseSchema } },
    },
    400: errorResponse('The request is invalid'),
    409: errorResponse('The idempotency key was already used for a different request'),
    422: errorResponse('The calculation could not be performed'),
    500: errorResponse('The request could not be completed'),
  };
}

function errorResponse(description: string): ResponseConfig {
  return {
    description,
    headers: correlationHeader,
    content: { 'application/json': { schema: apiErrorSchema } },
  };
}
