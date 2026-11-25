import type { CalculationId } from '../../domain/calculation-id.js';
import type { HistorySummary } from './history-summary.js';

// Inbound read port.
export abstract class CalculationHistory {
  abstract listRecent(limit: number): Promise<ReadonlyArray<HistorySummary>>;

  abstract findById(calculationId: CalculationId): Promise<HistorySummary | undefined>;
}
