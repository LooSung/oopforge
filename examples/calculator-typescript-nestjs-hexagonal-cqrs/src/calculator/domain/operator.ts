export const OPERATOR_NAMES = ['ADD', 'SUBTRACT', 'MULTIPLY', 'DIVIDE'] as const;

export type OperatorName = (typeof OPERATOR_NAMES)[number];

type Arithmetic = (a: number, b: number) => number;

export class Operator {
  static readonly ADD = new Operator('ADD', (a, b) => a + b);
  static readonly SUBTRACT = new Operator('SUBTRACT', (a, b) => a - b);
  static readonly MULTIPLY = new Operator('MULTIPLY', (a, b) => a * b);
  static readonly DIVIDE = new Operator('DIVIDE', divide);

  private static readonly BY_NAME: Readonly<Record<OperatorName, Operator>> = {
    ADD: Operator.ADD,
    SUBTRACT: Operator.SUBTRACT,
    MULTIPLY: Operator.MULTIPLY,
    DIVIDE: Operator.DIVIDE,
  };

  private constructor(
    public readonly name: OperatorName,
    private readonly arithmetic: Arithmetic,
  ) {}

  static of(name: OperatorName): Operator {
    return Operator.BY_NAME[name];
  }

  apply(a: number, b: number): number {
    return this.arithmetic(a, b);
  }
}

function divide(a: number, b: number): number {
  if (b === 0) {
    throw new RangeError('division by zero');
  }
  return a / b;
}
