import type { RouteHandler } from './correlationAuditFilter';
import { withCorrelationAudit } from './correlationAuditFilter';
import { buildOpenApiDocument } from './openApiDocument';
import { withWebErrorHandling } from './webErrorHandler';

const document = buildOpenApiDocument();

// GET /v3/api-docs, re-exported by src/app/v3/api-docs/route.ts. Correlated
// like every response, but not audited: reading the contract changes nothing.
export const GET: RouteHandler = withCorrelationAudit(
  withWebErrorHandling(async () => Response.json(document)),
);
