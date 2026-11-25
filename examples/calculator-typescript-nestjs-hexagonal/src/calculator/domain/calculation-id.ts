import { DomainRuleViolation } from './domain-rule-violation.js';

const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

export class CalculationId {
  private constructor(readonly value: string) {}

  static generate(): CalculationId {
    return new CalculationId(crypto.randomUUID());
  }

  static of(raw: string): CalculationId {
    if (!UUID.test(raw)) {
      throw new DomainRuleViolation('calculation id must be a UUID');
    }
    return new CalculationId(raw.toLowerCase());
  }

  equals(other: CalculationId): boolean {
    return this.value === other.value;
  }

  toString(): string {
    return this.value;
  }
}
