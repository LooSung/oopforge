import type { Calculation } from '../../domain/calculation';

export interface CalculationRepository {
  save(calculation: Calculation): void;
}
