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

// Module-level, not on globalThis: a graph that outlived a module re-evaluation
// would run stale code. Each evaluation starts with an empty in-memory store.
export const calculatorConfig: CalculatorConfig = createCalculatorConfig();
