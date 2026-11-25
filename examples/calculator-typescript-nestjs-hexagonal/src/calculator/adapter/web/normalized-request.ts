import type { CalculateCommand } from '../../application/provided/calculate.js';
import { Operator } from '../../domain/operator.js';
import type { CalculateRequest } from './calculate.request.js';

export class NormalizedRequest {
  private constructor(
    readonly operandA: number,
    readonly operator: Operator,
    readonly operandB: number,
  ) {}

  static from(request: CalculateRequest): NormalizedRequest {
    return new NormalizedRequest(
      normalizeZero(request.operandA),
      Operator.of(request.operator),
      normalizeZero(request.operandB),
    );
  }

  equals(other: NormalizedRequest): boolean {
    return this.operandA === other.operandA
      && this.operator === other.operator
      && this.operandB === other.operandB;
  }

  toCommand(): CalculateCommand {
    return { operandA: this.operandA, operator: this.operator, operandB: this.operandB };
  }
}

// -0 === 0, so this turns -0 into 0 and a replay echoes the same operands.
function normalizeZero(value: number): number {
  return value === 0 ? 0 : value;
}
