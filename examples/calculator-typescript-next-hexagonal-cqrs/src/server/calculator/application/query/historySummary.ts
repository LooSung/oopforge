import type { Calculation } from '../../domain/calculation';

// performedAt is an ISO-8601 string so the read model holds no mutable Date.
export class HistorySummary {
  private constructor(
    public readonly calculationId: string,
    public readonly operandA: number,
    public readonly operandB: number,
    public readonly operator: string,
    public readonly result: number,
    public readonly performedAt: string,
  ) {}

  static from(calculation: Calculation): HistorySummary {
    return new HistorySummary(
      calculation.id.value,
      calculation.operandA,
      calculation.operandB,
      calculation.operator.name.toLowerCase(),
      calculation.result,
      calculation.performedAt.toISOString(),
    );
  }
}
