import { expect, it } from 'vitest';

import { CalculationStore } from '../../../../../src/server/calculator/adapter/persistence/calculationStore';
import { InMemoryCalculationRepository } from '../../../../../src/server/calculator/adapter/persistence/inMemoryCalculationRepository';
import type { Calculate } from '../../../../../src/server/calculator/application/command/calculate';
import { CalculateCommandService } from '../../../../../src/server/calculator/application/command/calculateCommandService';
import { CalculationId } from '../../../../../src/server/calculator/domain/calculationId';
import { Operator } from '../../../../../src/server/calculator/domain/operator';

it('returnsIdNotReadModel', () => {
  const service: Calculate = new CalculateCommandService(new InMemoryCalculationRepository(new CalculationStore()));

  const id = service.handle({ operandA: 10, operator: Operator.ADD, operandB: 5 });

  expect(id).toBeInstanceOf(CalculationId);
  expect(id.value).toEqual(expect.any(String));
});
