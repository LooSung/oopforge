import { expect, it } from 'vitest';

import { Calculation } from '../../../../src/server/calculator/domain/calculation';
import { CalculationId } from '../../../../src/server/calculator/domain/calculationId';
import { Operator } from '../../../../src/server/calculator/domain/operator';

it('performsAddition', () => {
  const calculation = Calculation.perform(CalculationId.generate(), 2, Operator.ADD, 3);

  expect(calculation.result).toBe(5.0);
});

it('divideByZeroThrows', () => {
  expect(() => Calculation.perform(CalculationId.generate(), 1, Operator.DIVIDE, 0)).toThrow(RangeError);
});
