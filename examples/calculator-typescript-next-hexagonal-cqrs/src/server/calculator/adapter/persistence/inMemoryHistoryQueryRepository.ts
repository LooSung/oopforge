import type { HistoryQueryRepository } from '../../application/query/historyQueryRepository';
import type { HistorySummary } from '../../application/query/historySummary';
import type { CalculationId } from '../../domain/calculationId';
import type { CalculationStore } from './calculationStore';

export class InMemoryHistoryQueryRepository implements HistoryQueryRepository {
  constructor(private readonly calculationStore: CalculationStore) {}

  listRecent(limit: number): ReadonlyArray<HistorySummary> {
    if (limit <= 0) {
      throw new RangeError('limit must be positive');
    }
    return this.calculationStore.historySnapshot().slice(-limit).reverse();
  }

  findById(calculationId: CalculationId): HistorySummary | undefined {
    const target = calculationId.value;
    const newestFirst = this.calculationStore.historySnapshot().slice().reverse();
    return newestFirst.find((summary) => summary.calculationId === target);
  }
}
