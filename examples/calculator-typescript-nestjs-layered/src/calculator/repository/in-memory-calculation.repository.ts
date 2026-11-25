import { Injectable } from '@nestjs/common';

import type { Calculation } from '../domain/calculation.js';
import type { CalculationId } from '../domain/calculation-id.js';
import { CalculationRepository } from './calculation.repository.js';

@Injectable()
export class InMemoryCalculationRepository extends CalculationRepository {
  // Keyed by the id's string: a Map compares object keys by identity, not by value.
  private readonly calculations = new Map<string, Calculation>();

  async save(calculation: Calculation): Promise<void> {
    this.calculations.set(calculation.id.value, calculation);
  }

  async findById(id: CalculationId): Promise<Calculation | undefined> {
    return this.calculations.get(id.value);
  }
}
