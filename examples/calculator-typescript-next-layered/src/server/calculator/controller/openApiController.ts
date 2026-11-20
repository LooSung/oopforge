import { OpenAPIRegistry, OpenApiGeneratorV3 } from '@asteasolutions/zod-to-openapi';

import { CalculateRequest } from './dto/calculateRequest';
import { CalculationResponse } from './dto/calculationResponse';

type OpenApiDocument = ReturnType<OpenApiGeneratorV3['generateDocument']>;

export function GET(): Response {
  return Response.json(buildOpenApiDocument());
}

function buildOpenApiDocument(): OpenApiDocument {
  const registry = new OpenAPIRegistry();
  registerCalculate(registry);
  return new OpenApiGeneratorV3(registry.definitions).generateDocument({
    openapi: '3.0.1',
    info: { title: 'Calculator (layered 3-tier)', version: '0.1.0' },
  });
}

function registerCalculate(registry: OpenAPIRegistry): void {
  registry.registerPath({
    method: 'post',
    path: '/api/v1/calculations',
    tags: ['Calculator'],
    summary: 'Perform a calculation',
    request: { body: { content: { 'application/json': { schema: CalculateRequest } } } },
    responses: {
      201: { description: 'Created', content: { 'application/json': { schema: CalculationResponse } } },
      400: { description: 'Malformed JSON or a body that fails validation' },
    },
  });
}
