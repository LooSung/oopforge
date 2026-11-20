import type { Calculation } from '../domain/calculation';
import type { CalculationId } from '../domain/calculationId';
import type { CalculationRepository } from './calculationRepository';

export class InMemoryCalculationRepository implements CalculationRepository {
  // Keyed by the id's string: a Map compares object keys by identity, not by value.
  private readonly calculations = new Map<string, Calculation>();

  async save(calculation: Calculation): Promise<void> {
    this.calculations.set(calculation.id.value, calculation);
  }

  async findById(id: CalculationId): Promise<Calculation | undefined> {
    return this.calculations.get(id.value);
  }
}
