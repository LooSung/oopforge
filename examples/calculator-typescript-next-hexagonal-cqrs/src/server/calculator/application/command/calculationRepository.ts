import type { Calculation } from '../../domain/calculation';

// Promises even for the in-memory adapter: every durable Node.js driver is
// asynchronous, and swapping the adapter must not change this port or the service.
export interface CalculationRepository {
  save(calculation: Calculation): Promise<void>;
}
