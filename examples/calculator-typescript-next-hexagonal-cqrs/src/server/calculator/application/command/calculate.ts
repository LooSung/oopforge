import type { CalculationId } from '../../domain/calculationId';
import type { Operator } from '../../domain/operator';

export interface CalculateCommand {
  readonly operandA: number;
  readonly operator: Operator;
  readonly operandB: number;
}

// Returns only the new aggregate's id, never read-shaped data, to keep the
// command/query split honest.
export interface Calculate {
  handle(command: CalculateCommand): CalculationId;
}
