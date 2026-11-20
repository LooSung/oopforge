import type { Calculation } from '../../domain/calculation';
import type { CalculationId } from '../../domain/calculationId';

// Ports return promises even though the reference adapter is in-memory: every
// durable Node.js driver is asynchronous, and swapping the adapter must not
// change the port or the application service.
export interface CalculationRepository {
  save(calculation: Calculation): Promise<void>;
  findById(id: CalculationId): Promise<Calculation | undefined>;
}
