import { CalculationStore } from '../../adapter/persistence/calculation-store.js';
import { InMemoryCalculationRepository } from '../../adapter/persistence/in-memory-calculation.repository.js';
import { CalculationId } from '../../domain/calculation-id.js';
import { Operator } from '../../domain/operator.js';
import type { Calculate } from './calculate.js';
import { CalculateCommandService } from './calculate-command.service.js';

it('returnsIdNotReadModel', async () => {
  const service: Calculate = new CalculateCommandService(new InMemoryCalculationRepository(new CalculationStore()));

  const id = await service.handle({ operandA: 10, operator: Operator.ADD, operandB: 5 });

  expect(id).toBeInstanceOf(CalculationId);
  expect(id.value).toEqual(expect.any(String));
});
