import { Calculation } from './calculation.js';
import { CalculationId } from './calculation-id.js';
import { Operator } from './operator.js';

it('performsAddition', () => {
  const calculation = Calculation.perform(CalculationId.generate(), 2, Operator.ADD, 3);

  expect(calculation.result).toBe(5.0);
});

it('divideByZeroThrows', () => {
  expect(() => Calculation.perform(CalculationId.generate(), 1, Operator.DIVIDE, 0)).toThrow(RangeError);
});
