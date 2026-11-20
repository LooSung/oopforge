import { DomainRuleViolation } from './domainRuleViolation';

export const OPERATOR_NAMES = ['ADD', 'SUBTRACT', 'MULTIPLY', 'DIVIDE'] as const;

export type OperatorName = (typeof OPERATOR_NAMES)[number];

type Operation = (a: number, b: number) => number;

// Each operator carries its own behaviour, so adding one never touches a switch.
export class Operator {
  static readonly ADD = new Operator('ADD', (a, b) => a + b);
  static readonly SUBTRACT = new Operator('SUBTRACT', (a, b) => a - b);
  static readonly MULTIPLY = new Operator('MULTIPLY', (a, b) => a * b);
  static readonly DIVIDE = new Operator('DIVIDE', divide);

  private constructor(
    readonly name: OperatorName,
    private readonly operation: Operation,
  ) {}

  static of(name: OperatorName): Operator {
    return OPERATORS_BY_NAME[name];
  }

  apply(a: number, b: number): number {
    return this.operation(a, b);
  }
}

function divide(a: number, b: number): number {
  if (b === 0) {
    throw new DomainRuleViolation('division by zero');
  }
  return a / b;
}

const OPERATORS_BY_NAME: Readonly<Record<OperatorName, Operator>> = {
  ADD: Operator.ADD,
  SUBTRACT: Operator.SUBTRACT,
  MULTIPLY: Operator.MULTIPLY,
  DIVIDE: Operator.DIVIDE,
};
