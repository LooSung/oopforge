import type { Calculation } from '../domain/calculation';
import type { CalculationId } from '../domain/calculationId';

export interface CalculationRepository {
  save(calculation: Calculation): void;

  findById(id: CalculationId): Calculation | undefined;
}
