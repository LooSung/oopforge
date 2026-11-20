import type { CalculationId } from '../../domain/calculationId';
import type { CalculationHistory } from './calculationHistory';
import type { HistoryQueryRepository } from './historyQueryRepository';
import type { HistorySummary } from './historySummary';

export class HistoryQueryService implements CalculationHistory {
  constructor(private readonly queryRepository: HistoryQueryRepository) {}

  listRecent(limit: number): ReadonlyArray<HistorySummary> {
    return this.queryRepository.listRecent(limit);
  }

  findById(calculationId: CalculationId): HistorySummary | undefined {
    return this.queryRepository.findById(calculationId);
  }
}
