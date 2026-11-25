import type { CalculationId } from '../../domain/calculation-id.js';
import type { Operator } from '../../domain/operator.js';

export interface CalculateCommand {
  readonly operandA: number;
  readonly operator: Operator;
  readonly operandB: number;
}

// Inbound write port. Returns only the new aggregate's id, never read-shaped
// data, to keep the command/query split honest. An abstract class, not an
// interface, because Nest injects by a runtime token.
export abstract class Calculate {
  abstract handle(command: CalculateCommand): Promise<CalculationId>;
}
