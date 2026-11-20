import type { Calculation } from '../domain/calculation';
import type { CalculationId } from '../domain/calculationId';

// Promises even for the in-memory adapter: every durable Node.js driver is
// asynchronous, and swapping the adapter must not change this interface or the service.
export interface CalculationRepository {
  save(calculation: Calculation): Promise<void>;

  findById(id: CalculationId): Promise<Calculation | undefined>;
}
