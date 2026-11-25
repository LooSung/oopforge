import { BadRequestException, Catch, HttpException, Logger, type ArgumentsHost } from '@nestjs/common';
import { BaseExceptionFilter } from '@nestjs/core';
import type { Response } from 'express';

import { DomainRuleViolation } from '../../domain/domain-rule-violation.js';
import type { ApiError } from './api-error.js';
import { IdempotencyConflictError } from './idempotency-conflict.error.js';
import { InvalidWebRequestError } from './invalid-web-request.error.js';

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

// Global, so it also sees malformed JSON from the body parser and schema
// failures from the validation pipe. Known failures get a safe body; other
// HTTP errors, such as a 404, keep Nest's answer; anything else is logged
// without its details and hidden behind internal_error.
@Catch()
export class WebExceptionFilter extends BaseExceptionFilter {
  private readonly logger = new Logger('WebExceptionFilter');

  override catch(error: unknown, host: ArgumentsHost): void {
    const response = host.switchToHttp().getResponse<Response>();
    const safe = safeError(error);
    if (safe === undefined) {
      super.catch(error, host);
      return;
    }
    if (safe === INTERNAL_ERROR) {
      this.logger.error(`Unexpected calculation request failure correlationId=${response.locals.correlationId}`);
    }
    response.status(safe.status).json(safe.body);
  }
}

export function safeError(error: unknown): SafeError | undefined {
  if (error instanceof InvalidWebRequestError || error instanceof BadRequestException) {
    return INVALID_REQUEST;
  }
  if (error instanceof IdempotencyConflictError) {
    return IDEMPOTENCY_CONFLICT;
  }
  if (error instanceof DomainRuleViolation) {
    return CALCULATION_REJECTED;
  }
  return error instanceof HttpException ? undefined : INTERNAL_ERROR;
}
