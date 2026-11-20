import type { CalculationId } from './calculationId';
import type { Operator } from './operator';

export class Calculation {
  private constructor(
    public readonly id: CalculationId,
    public readonly operandA: number,
    public readonly operator: Operator,
    public readonly operandB: number,
    public readonly result: number,
  ) {}

  static perform(id: CalculationId, operandA: number, operator: Operator, operandB: number): Calculation {
    const result = operator.apply(operandA, operandB);
    return new Calculation(id, operandA, operator, operandB, result);
  }
}
