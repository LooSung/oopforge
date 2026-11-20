import type { Operator } from '../../domain/operator';

export interface CalculateCommand {
  readonly operandA: number;
  readonly operator: Operator;
  readonly operandB: number;
}

export interface CalculationResult {
  readonly calculationId: string;
  readonly operandA: number;
  readonly operator: Operator;
  readonly operandB: number;
  readonly result: number;
}

export interface Calculate {
  handle(command: CalculateCommand): Promise<CalculationResult>;
}
