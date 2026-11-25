import type { CalculationId } from './calculation-id.js';
import { CalculationPerformed } from './calculation-performed.js';
import type { DomainEvent } from './domain-event.js';
import type { Operator } from './operator.js';

export class Calculation {
  private readonly events: DomainEvent[] = [];

  private constructor(
    readonly id: CalculationId,
    readonly operandA: number,
    readonly operator: Operator,
    readonly operandB: number,
    readonly result: number,
  ) {}

  static perform(id: CalculationId, operandA: number, operator: Operator, operandB: number): Calculation {
    const result = operator.apply(operandA, operandB);
    const calculation = new Calculation(id, operandA, operator, operandB, result);
    calculation.record(new CalculationPerformed(id, result));
    return calculation;
  }

  // ReadonlyArray is compile-time only: the caller gets a fresh array, and the
  // Aggregate's own list is emptied so each event is drained exactly once.
  popEvents(): ReadonlyArray<DomainEvent> {
    return this.events.splice(0);
  }

  private record(event: DomainEvent): void {
    this.events.push(event);
  }
}
