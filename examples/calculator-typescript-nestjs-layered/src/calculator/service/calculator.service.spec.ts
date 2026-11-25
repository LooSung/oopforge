import { Operator } from '../domain/operator.js';
import { InMemoryCalculationRepository } from '../repository/in-memory-calculation.repository.js';
import { CalculatorService } from './calculator.service.js';

it('calculatesProduct', async () => {
  const service = new CalculatorService(new InMemoryCalculationRepository());

  const result = await service.calculate({ operandA: 6, operator: Operator.MULTIPLY, operandB: 7 });

  expect(result.result).toBe(42.0);
  expect(result.calculationId).toEqual(expect.any(String));
});
