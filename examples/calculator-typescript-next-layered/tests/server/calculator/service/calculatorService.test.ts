import { expect, it } from 'vitest';

import { Operator } from '../../../../src/server/calculator/domain/operator';
import { InMemoryCalculationRepository } from '../../../../src/server/calculator/repository/inMemoryCalculationRepository';
import { CalculatorService } from '../../../../src/server/calculator/service/calculatorService';

it('calculatesProduct', () => {
  const service = new CalculatorService(new InMemoryCalculationRepository());

  const result = service.calculate({ operandA: 6, operator: Operator.MULTIPLY, operandB: 7 });

  expect(result.result).toBe(42.0);
  expect(result.calculationId).toEqual(expect.any(String));
});
