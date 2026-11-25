import type { Calculation } from '../../domain/calculation.js';

// Outbound write port. Promises even for the in-memory adapter: every durable
// Node.js driver is asynchronous, and swapping the adapter must not change this
// port or the service.
export abstract class CalculationRepository {
  abstract save(calculation: Calculation): Promise<void>;
}
