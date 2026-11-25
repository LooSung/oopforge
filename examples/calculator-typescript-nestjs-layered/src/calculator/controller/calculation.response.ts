export interface CalculationResponse {
  readonly calculationId: string;
  readonly operandA: number;
  readonly operator: string;
  readonly operandB: number;
  readonly result: number;
}
