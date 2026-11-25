import type { CalculationId } from '../../domain/calculation-id.js';
import type { HistorySummary } from './history-summary.js';

// Outbound read port. Promises for the same reason as the write port: a durable
// read store is asynchronous.
export abstract class HistoryQueryRepository {
  abstract listRecent(limit: number): Promise<ReadonlyArray<HistorySummary>>;

  abstract findById(calculationId: CalculationId): Promise<HistorySummary | undefined>;
}
