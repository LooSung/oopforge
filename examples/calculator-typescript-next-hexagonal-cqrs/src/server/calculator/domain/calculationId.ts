const UUID_PATTERN = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

export class CalculationId {
  private constructor(public readonly value: string) {}

  static generate(): CalculationId {
    return new CalculationId(crypto.randomUUID());
  }

  static of(raw: string): CalculationId {
    if (!UUID_PATTERN.test(raw)) {
      throw new RangeError('calculation id must be a UUID');
    }
    return new CalculationId(raw.toLowerCase());
  }
}
