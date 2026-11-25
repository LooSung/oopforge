import type { Operator } from '../../domain/operator.js';

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

// The inbound port. An abstract class, not an interface, because Nest injects
// by a runtime token and an interface does not exist at runtime.
export abstract class Calculate {
  abstract handle(command: CalculateCommand): Promise<CalculationResult>;
}
