import { Injectable } from '@nestjs/common';

import { Calculate } from '../../application/provided/calculate.js';
import type { CalculateRequest } from './calculate.request.js';
import { toCalculationResponse, type CalculationResponse } from './calculation.response.js';
import { IdempotencyStore } from './idempotency.store.js';
import { NormalizedRequest } from './normalized-request.js';

@Injectable()
export class IdempotentCalculationHandler {
  constructor(
    private readonly calculate: Calculate,
    private readonly idempotencyStore: IdempotencyStore,
  ) {}

  async handle(request: CalculateRequest, idempotencyKey: string | null): Promise<CalculationResponse> {
    const normalized = NormalizedRequest.from(request);
    return this.idempotencyStore.execute(idempotencyKey, normalized, () => this.perform(normalized));
  }

  private async perform(request: NormalizedRequest): Promise<CalculationResponse> {
    return toCalculationResponse(await this.calculate.handle(request.toCommand()));
  }
}
