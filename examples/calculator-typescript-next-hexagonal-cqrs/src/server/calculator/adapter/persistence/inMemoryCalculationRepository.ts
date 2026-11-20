import type { CalculationRepository } from '../../application/command/calculationRepository';
import { HistorySummary } from '../../application/query/historySummary';
import type { Calculation } from '../../domain/calculation';
import type { CalculationStore } from './calculationStore';

export class InMemoryCalculationRepository implements CalculationRepository {
  constructor(private readonly calculationStore: CalculationStore) {}

  save(calculation: Calculation): void {
    this.calculationStore.putCalculation(calculation);
    this.calculationStore.appendHistory(HistorySummary.from(calculation));
  }
}
