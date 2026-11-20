import type { HistorySummary } from '../../application/query/historySummary';
import type { Calculation } from '../../domain/calculation';

// Both adapters share this one store so a command is visible to later queries.
export class CalculationStore {
  // Keyed by the id's string: a Map compares object keys by identity, not by value.
  private readonly calculations = new Map<string, Calculation>();
  private readonly history: HistorySummary[] = [];

  putCalculation(calculation: Calculation): void {
    this.calculations.set(calculation.id.value, calculation);
  }

  appendHistory(summary: HistorySummary): void {
    this.history.push(summary);
  }

  historySnapshot(): ReadonlyArray<HistorySummary> {
    return [...this.history];
  }
}
