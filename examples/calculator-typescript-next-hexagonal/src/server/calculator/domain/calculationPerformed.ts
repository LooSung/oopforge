import type { CalculationId } from './calculationId';
import { DomainEvent } from './domainEvent';

export class CalculationPerformed extends DomainEvent {
  constructor(
    readonly calculationId: CalculationId,
    readonly result: number,
  ) {
    super();
  }
}
