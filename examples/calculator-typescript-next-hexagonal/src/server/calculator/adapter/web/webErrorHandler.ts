import { DomainRuleViolation } from '../../domain/domainRuleViolation';
import type { ApiError } from './apiError';
import type { CorrelatedHandler } from './correlationAuditFilter';
import { IdempotencyConflictError } from './idempotencyConflictError';
import { InvalidWebRequestError } from './invalidWebRequestError';

export interface SafeError {
  readonly status: number;
  readonly body: ApiError;
}

const INVALID_REQUEST: SafeError = {
  status: 400,
  body: { code: 'invalid_request', message: 'The request is invalid.' },
};
const IDEMPOTENCY_CONFLICT: SafeError = {
  status: 409,
  body: {
    code: 'idempotency_conflict',
    message: 'The idempotency key was already used for a different request.',
  },
};
const CALCULATION_REJECTED: SafeError = {
  status: 422,
  body: { code: 'calculation_rejected', message: 'The calculation could not be performed.' },
};
const INTERNAL_ERROR: SafeError = {
  status: 500,
  body: { code: 'internal_error', message: 'The request could not be completed.' },
};

// Only known failures get a specific answer; anything else is logged without
// its details and hidden behind internal_error.
export function safeError(error: unknown, correlationId?: string): SafeError {
  if (error instanceof InvalidWebRequestError) {
    return INVALID_REQUEST;
  }
  if (error instanceof IdempotencyConflictError) {
    return IDEMPOTENCY_CONFLICT;
  }
  if (error instanceof DomainRuleViolation) {
    return CALCULATION_REJECTED;
  }
  console.error('Unexpected calculation request failure', { correlationId });
  return INTERNAL_ERROR;
}

export function withWebErrorHandling(handler: CorrelatedHandler): CorrelatedHandler {
  return async (request, correlationId) => {
    try {
      return await handler(request, correlationId);
    } catch (error) {
      const { status, body } = safeError(error, correlationId);
      return Response.json(body, { status });
    }
  };
}
