import type { CalculationId } from '../../domain/calculationId';
import type { HistorySummary } from './historySummary';

export interface HistoryQueryRepository {
  listRecent(limit: number): ReadonlyArray<HistorySummary>;

  findById(calculationId: CalculationId): HistorySummary | undefined;
}
