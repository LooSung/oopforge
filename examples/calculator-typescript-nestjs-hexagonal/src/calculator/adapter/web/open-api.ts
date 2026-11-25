import { applyDecorators, type INestApplication } from '@nestjs/common';
import { ApiResponse, DocumentBuilder, SwaggerModule, type OpenAPIObject } from '@nestjs/swagger';

import { apiErrorSchema } from './api-error.js';
import { calculationResponseSchema } from './calculation.response.js';
import { CORRELATION_HEADER } from './correlation-audit.middleware.js';

const CORRELATION_RESPONSE_HEADER = {
  [CORRELATION_HEADER]: {
    description: 'Echoed or generated correlation id',
    schema: { type: 'string' as const },
  },
};

// Every documented answer of POST /calculations: the zod schemas become the
// CalculationResponse and ApiError components.
export function ApiCalculationResponses(): MethodDecorator {
  return applyDecorators(
    ApiResponse({
      status: 201,
      description: 'Calculation performed, or the stored result replayed for a repeated key',
      headers: CORRELATION_RESPONSE_HEADER,
      standardSchema: calculationResponseSchema,
    }),
    errorResponse(400, 'The request is invalid'),
    errorResponse(409, 'The idempotency key was already used for a different request'),
    errorResponse(422, 'The calculation could not be performed'),
    errorResponse(500, 'The request could not be completed'),
  );
}

export function buildOpenApiDocument(app: INestApplication): OpenAPIObject {
  const config = new DocumentBuilder()
    .setTitle('Calculator (TypeScript NestJS hexagonal)')
    .setVersion('0.1.0')
    .build();
  return SwaggerModule.createDocument(app, config);
}

function errorResponse(status: number, description: string): MethodDecorator & ClassDecorator {
  return ApiResponse({ status, description, headers: CORRELATION_RESPONSE_HEADER, standardSchema: apiErrorSchema });
}
