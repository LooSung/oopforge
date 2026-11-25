import { Injectable } from '@nestjs/common';

import { CalculationRepository } from '../../application/command/calculation.repository.js';
import { HistorySummary } from '../../application/query/history-summary.js';
import type { Calculation } from '../../domain/calculation.js';
import { CalculationStore } from './calculation-store.js';

@Injectable()
export class InMemoryCalculationRepository extends CalculationRepository {
  constructor(private readonly calculationStore: CalculationStore) {
    super();
  }

  async save(calculation: Calculation): Promise<void> {
    this.calculationStore.putCalculation(calculation);
    this.calculationStore.appendHistory(HistorySummary.from(calculation));
  }
}
