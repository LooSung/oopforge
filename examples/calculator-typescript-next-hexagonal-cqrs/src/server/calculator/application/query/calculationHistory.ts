import type { CalculationId } from '../../domain/calculationId';
import type { HistorySummary } from './historySummary';

export interface CalculationHistory {
  listRecent(limit: number): Promise<ReadonlyArray<HistorySummary>>;

  findById(calculationId: CalculationId): Promise<HistorySummary | undefined>;
}
