import type { Calculate } from '../../application/provided/calculate';
import type { CalculateRequest } from './calculateRequest';
import type { CalculationResponse } from './calculationResponse';
import { toCalculationResponse } from './calculationResponse';
import type { IdempotencyStore } from './idempotencyStore';
import { NormalizedRequest } from './normalizedRequest';

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
