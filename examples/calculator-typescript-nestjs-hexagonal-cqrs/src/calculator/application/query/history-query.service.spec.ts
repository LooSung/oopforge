import { CalculationStore } from '../../adapter/persistence/calculation-store.js';
import { InMemoryCalculationRepository } from '../../adapter/persistence/in-memory-calculation.repository.js';
import { InMemoryHistoryQueryRepository } from '../../adapter/persistence/in-memory-history-query.repository.js';
import { Operator } from '../../domain/operator.js';
import type { Calculate } from '../command/calculate.js';
import { CalculateCommandService } from '../command/calculate-command.service.js';
import type { CalculationHistory } from './calculation-history.js';
import { HistoryQueryService } from './history-query.service.js';

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
