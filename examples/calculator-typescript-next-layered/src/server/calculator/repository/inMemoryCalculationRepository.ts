import type { Calculation } from '../domain/calculation';
import type { CalculationId } from '../domain/calculationId';
import type { CalculationRepository } from './calculationRepository';

export class InMemoryCalculationRepository implements CalculationRepository {
  // Keyed by the id's string: a Map compares object keys by identity, not by value.
  private readonly calculations = new Map<string, Calculation>();

  save(calculation: Calculation): void {
    this.calculations.set(calculation.id.value, calculation);
  }

  findById(id: CalculationId): Calculation | undefined {
    return this.calculations.get(id.value);
  }
}
