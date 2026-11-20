import { expect, it } from 'vitest';

import { CalculationStore } from '../../../../../src/server/calculator/adapter/persistence/calculationStore';
import { InMemoryCalculationRepository } from '../../../../../src/server/calculator/adapter/persistence/inMemoryCalculationRepository';
import { InMemoryHistoryQueryRepository } from '../../../../../src/server/calculator/adapter/persistence/inMemoryHistoryQueryRepository';
import type { Calculate } from '../../../../../src/server/calculator/application/command/calculate';
import { CalculateCommandService } from '../../../../../src/server/calculator/application/command/calculateCommandService';
import type { CalculationHistory } from '../../../../../src/server/calculator/application/query/calculationHistory';
import { HistoryQueryService } from '../../../../../src/server/calculator/application/query/historyQueryService';
import { Operator } from '../../../../../src/server/calculator/domain/operator';

it('listsHistoryMostRecentFirstAfterCommands', async () => {
  const store = new CalculationStore();
  const command: Calculate = new CalculateCommandService(new InMemoryCalculationRepository(store));
  const query: CalculationHistory = new HistoryQueryService(new InMemoryHistoryQueryRepository(store));

  await command.handle({ operandA: 1, operator: Operator.ADD, operandB: 2 });
  await command.handle({ operandA: 5, operator: Operator.MULTIPLY, operandB: 3 });

  const history = await query.listRecent(10);

  expect(history).toHaveLength(2);
  expect(history[0]?.result).toBe(15.0);
  expect(history[1]?.result).toBe(3.0);
});
