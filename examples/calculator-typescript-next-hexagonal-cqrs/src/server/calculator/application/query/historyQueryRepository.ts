import type { CalculationId } from '../../domain/calculationId';
import type { HistorySummary } from './historySummary';

// Promises for the same reason as the write port: a durable read store is asynchronous.
export interface HistoryQueryRepository {
  listRecent(limit: number): Promise<ReadonlyArray<HistorySummary>>;

  findById(calculationId: CalculationId): Promise<HistorySummary | undefined>;
}
