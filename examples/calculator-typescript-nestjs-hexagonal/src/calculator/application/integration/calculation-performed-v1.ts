export interface CalculationPerformedV1Fields {
  readonly schemaVersion: number;
  readonly calculationId: string;
  readonly result: number;
  readonly occurredAt: string;
}

// The versioned integration contract. It is a class, not a plain object, so a
// consumer can narrow an `unknown` outbox payload with `instanceof`.
export class CalculationPerformedV1 {
  static readonly SCHEMA_VERSION = 1;
  // Explicit, because production bundles may minify class names.
  static readonly EVENT_TYPE = 'CalculationPerformedV1';

  private constructor(
    readonly schemaVersion: number,
    readonly calculationId: string,
    readonly result: number,
    readonly occurredAt: string,
  ) {}

  static of(fields: CalculationPerformedV1Fields): CalculationPerformedV1 {
    if (fields.schemaVersion !== CalculationPerformedV1.SCHEMA_VERSION) {
      throw new RangeError('schemaVersion must be 1');
    }
    const { schemaVersion, calculationId, result, occurredAt } = fields;
    return Object.freeze(new CalculationPerformedV1(schemaVersion, calculationId, result, occurredAt));
  }
}
