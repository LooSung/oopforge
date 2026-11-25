import type { Calculation } from '../../domain/calculation.js';
import type { CalculationId } from '../../domain/calculation-id.js';

// Ports return promises even though the reference adapter is in-memory: every
// durable Node.js driver is asynchronous, and swapping the adapter must not
// change the port or the application service.
export abstract class CalculationRepository {
  abstract save(calculation: Calculation): Promise<void>;

  abstract findById(id: CalculationId): Promise<Calculation | undefined>;
}
