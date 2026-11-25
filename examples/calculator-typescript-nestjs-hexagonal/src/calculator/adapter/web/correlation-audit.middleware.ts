import type { NextFunction, Request, RequestHandler, Response } from 'express';

import type { InMemoryAuditAdapter } from '../audit/in-memory-audit.adapter.js';

export const CORRELATION_HEADER = 'X-Correlation-Id';

const SAFE_CORRELATION_ID = /^[A-Za-z0-9._:-]{1,128}$/;

const OUTCOMES: ReadonlyMap<number, string> = new Map([
  [201, 'created'],
  [400, 'invalid_request'],
  [409, 'idempotency_conflict'],
  [422, 'calculation_rejected'],
]);

export interface AuditedRoute {
  readonly method: string;
  readonly path: string;
  readonly action: string;
}

// Plain Express middleware, registered with app.use() before Nest's body parser
// and router: like Java's servlet filter it sees every request, malformed JSON
// included. The audit entry is written on 'finish', after the exception filter
// has set the final status.
export function correlationAudit(audit: InMemoryAuditAdapter, routes: ReadonlyArray<AuditedRoute>): RequestHandler {
  return (request: Request, response: Response, next: NextFunction): void => {
    const correlationId = correlationIdFrom(request.header(CORRELATION_HEADER));
    response.locals.correlationId = correlationId;
    response.setHeader(CORRELATION_HEADER, correlationId);
    const action = routes.find((route) => route.method === request.method && route.path === request.path)?.action;
    if (action !== undefined) {
      response.once('finish', () => audit.record(correlationId, action, outcome(response.statusCode)));
    }
    next();
  };
}

function correlationIdFrom(provided: string | undefined): string {
  if (provided === undefined) {
    return crypto.randomUUID();
  }
  const candidate = provided.trim();
  return SAFE_CORRELATION_ID.test(candidate) ? candidate : crypto.randomUUID();
}

function outcome(status: number): string {
  return OUTCOMES.get(status) ?? (status >= 500 ? 'failed' : 'completed');
}
