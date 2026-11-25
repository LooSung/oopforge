import { Injectable } from '@nestjs/common';

import { HistoryQueryRepository } from '../../application/query/history-query.repository.js';
import type { HistorySummary } from '../../application/query/history-summary.js';
import type { CalculationId } from '../../domain/calculation-id.js';
import { CalculationStore } from './calculation-store.js';

@Injectable()
export class InMemoryHistoryQueryRepository extends HistoryQueryRepository {
  constructor(private readonly calculationStore: CalculationStore) {
    super();
  }

  async listRecent(limit: number): Promise<ReadonlyArray<HistorySummary>> {
    if (limit <= 0) {
      throw new RangeError('limit must be positive');
    }
    return this.calculationStore.historySnapshot().slice(-limit).reverse();
  }

  async findById(calculationId: CalculationId): Promise<HistorySummary | undefined> {
    const target = calculationId.value;
    const newestFirst = this.calculationStore.historySnapshot().slice().reverse();
    return newestFirst.find((summary) => summary.calculationId === target);
  }
}
