import { Body, Controller, Headers, Post } from '@nestjs/common';
import { ApiHeader, ApiOperation } from '@nestjs/swagger';

import { calculateRequestSchema, type CalculateRequest } from './calculate.request.js';
import type { CalculationResponse } from './calculation.response.js';
import { CORRELATION_HEADER, type AuditedRoute } from './correlation-audit.middleware.js';
import { IDEMPOTENCY_KEY_HEADER, MAX_KEY_LENGTH } from './idempotency.store.js';
import { IdempotentCalculationHandler } from './idempotent-calculation.handler.js';
import { ApiCalculationResponses } from './open-api.js';

export const CALCULATIONS_PATH = 'calculations';

export const CALCULATION_CREATE: AuditedRoute = {
  method: 'POST',
  path: `/${CALCULATIONS_PATH}`,
  action: 'calculation.create',
};

@Controller(CALCULATIONS_PATH)
export class CalculatorController {
  constructor(private readonly calculationHandler: IdempotentCalculationHandler) {}

  @Post()
  @ApiOperation({ summary: 'Perform a calculation' })
  @ApiHeader({
    name: IDEMPOTENCY_KEY_HEADER,
    required: false,
    schema: { type: 'string', minLength: 1, maxLength: MAX_KEY_LENGTH },
  })
  @ApiHeader({ name: CORRELATION_HEADER, required: false })
  @ApiCalculationResponses()
  async calculate(
    @Body({ schema: calculateRequestSchema }) body: CalculateRequest,
    @Headers(IDEMPOTENCY_KEY_HEADER.toLowerCase()) idempotencyKey: string | undefined,
  ): Promise<CalculationResponse> {
    return this.calculationHandler.handle(body, idempotencyKey ?? null);
  }
}
