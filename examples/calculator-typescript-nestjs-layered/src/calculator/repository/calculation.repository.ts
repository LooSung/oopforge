import type { Calculation } from '../domain/calculation.js';
import type { CalculationId } from '../domain/calculation-id.js';

// An abstract class, not an interface: Nest injects by a runtime token, and an
// interface does not exist at runtime. Promises even for the in-memory adapter,
// because every durable Node.js driver is asynchronous.
export abstract class CalculationRepository {
  abstract save(calculation: Calculation): Promise<void>;

  abstract findById(id: CalculationId): Promise<Calculation | undefined>;
}
