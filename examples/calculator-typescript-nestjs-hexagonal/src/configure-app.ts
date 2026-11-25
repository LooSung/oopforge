import { StandardSchemaValidationPipe, type INestApplication } from '@nestjs/common';
import { SwaggerModule } from '@nestjs/swagger';

import { InMemoryAuditAdapter } from './calculator/adapter/audit/in-memory-audit.adapter.js';
import { CALCULATION_CREATE } from './calculator/adapter/web/calculator.controller.js';
import { correlationAudit } from './calculator/adapter/web/correlation-audit.middleware.js';
import { buildOpenApiDocument } from './calculator/adapter/web/open-api.js';
import { WebExceptionFilter } from './calculator/adapter/web/web-exception.filter.js';

// Shared by main.ts and the e2e tests, so both run the same middleware, pipes,
// filters, and documents. The correlation middleware goes first, before Nest
// registers its body parser on init().
export function configureApp(app: INestApplication): INestApplication {
  app.use(correlationAudit(app.get(InMemoryAuditAdapter), [CALCULATION_CREATE]));
  app.useGlobalPipes(new StandardSchemaValidationPipe());
  app.useGlobalFilters(new WebExceptionFilter(app.getHttpAdapter()));
  SwaggerModule.setup('swagger-ui', app, () => buildOpenApiDocument(app), {
    jsonDocumentUrl: 'v3/api-docs',
  });
  return app;
}
