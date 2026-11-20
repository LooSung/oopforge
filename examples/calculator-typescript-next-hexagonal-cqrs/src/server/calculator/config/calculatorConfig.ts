import 'server-only';

import { CalculationStore } from '../adapter/persistence/calculationStore';
import { InMemoryCalculationRepository } from '../adapter/persistence/inMemoryCalculationRepository';
import { InMemoryHistoryQueryRepository } from '../adapter/persistence/inMemoryHistoryQueryRepository';
import type { Calculate } from '../application/command/calculate';
import { CalculateCommandService } from '../application/command/calculateCommandService';
import type { CalculationHistory } from '../application/query/calculationHistory';
import { HistoryQueryService } from '../application/query/historyQueryService';

export interface CalculatorConfig {
  readonly calculate: Calculate;
  readonly calculationHistory: CalculationHistory;
}

export function createCalculatorConfig(): CalculatorConfig {
  const calculationStore = new CalculationStore();
  return {
    calculate: new CalculateCommandService(new InMemoryCalculationRepository(calculationStore)),
    calculationHistory: new HistoryQueryService(new InMemoryHistoryQueryRepository(calculationStore)),
  };
}

// `next dev` re-evaluates modules each time it compiles another route, which
// would drop an in-memory store held in a plain module variable.
const globalScope = globalThis as typeof globalThis & { oopforgeCalculatorConfig?: CalculatorConfig };

export const calculatorConfig: CalculatorConfig = (globalScope.oopforgeCalculatorConfig ??= createCalculatorConfig());
