import { Injectable } from '@nestjs/common';

import type { CalculationId } from '../../domain/calculation-id.js';
import { CalculationHistory } from './calculation-history.js';
import { HistoryQueryRepository } from './history-query.repository.js';
import type { HistorySummary } from './history-summary.js';

@Injectable()
export class HistoryQueryService extends CalculationHistory {
  constructor(private readonly queryRepository: HistoryQueryRepository) {
    super();
  }

  async listRecent(limit: number): Promise<ReadonlyArray<HistorySummary>> {
    return this.queryRepository.listRecent(limit);
  }

  async findById(calculationId: CalculationId): Promise<HistorySummary | undefined> {
    return this.queryRepository.findById(calculationId);
  }
}
