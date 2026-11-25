import type { CalculationId } from './calculation-id.js';
import { DomainEvent } from './domain-event.js';

export class CalculationPerformed extends DomainEvent {
  constructor(
    readonly calculationId: CalculationId,
    readonly result: number,
  ) {
    super();
  }
}
