import type { CalculationId } from '../../domain/calculationId';
import type { CalculationHistory } from './calculationHistory';
import type { HistoryQueryRepository } from './historyQueryRepository';
import type { HistorySummary } from './historySummary';

export class HistoryQueryService implements CalculationHistory {
  constructor(private readonly queryRepository: HistoryQueryRepository) {}

  async listRecent(limit: number): Promise<ReadonlyArray<HistorySummary>> {
    return this.queryRepository.listRecent(limit);
  }

  async findById(calculationId: CalculationId): Promise<HistorySummary | undefined> {
    return this.queryRepository.findById(calculationId);
  }
}
