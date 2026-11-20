import type { InMemoryAuditAdapter } from '../audit/inMemoryAuditAdapter';

export const CORRELATION_HEADER = 'X-Correlation-Id';

const SAFE_CORRELATION_ID = /^[A-Za-z0-9._:-]{1,128}$/;

const OUTCOMES: ReadonlyMap<number, string> = new Map([
  [201, 'created'],
  [400, 'invalid_request'],
  [409, 'idempotency_conflict'],
  [422, 'calculation_rejected'],
]);

export type RouteHandler = (request: Request) => Promise<Response>;

export type CorrelatedHandler = (request: Request, correlationId: string) => Promise<Response>;

export interface AuditTarget {
  readonly audit: InMemoryAuditAdapter;
  readonly action: string;
}

// A wrapper, not Next.js middleware: middleware runs on the Edge runtime and
// cannot share the in-memory audit store with the handler. It must stay the
// outermost wrapper so the header and the audit outcome see the final status.
export function withCorrelationAudit(handler: CorrelatedHandler, auditTarget?: AuditTarget): RouteHandler {
  return async (request) => {
    const correlationId = correlationIdFrom(request.headers.get(CORRELATION_HEADER));
    const response = await handler(request, correlationId);
    response.headers.set(CORRELATION_HEADER, correlationId);
    auditTarget?.audit.record(correlationId, auditTarget.action, outcome(response.status));
    return response;
  };
}

function correlationIdFrom(provided: string | null): string {
  if (provided === null) {
    return crypto.randomUUID();
  }
  const candidate = provided.trim();
  return SAFE_CORRELATION_ID.test(candidate) ? candidate : crypto.randomUUID();
}

function outcome(status: number): string {
  return OUTCOMES.get(status) ?? (status >= 500 ? 'failed' : 'completed');
}
