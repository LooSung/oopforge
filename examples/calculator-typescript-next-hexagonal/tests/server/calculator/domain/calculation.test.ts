import { expect, it } from 'vitest';
import { Calculation } from '../../../../src/server/calculator/domain/calculation';
import { CalculationId } from '../../../../src/server/calculator/domain/calculationId';
import { CalculationPerformed } from '../../../../src/server/calculator/domain/calculationPerformed';
import { DomainRuleViolation } from '../../../../src/server/calculator/domain/domainRuleViolation';
import { Operator } from '../../../../src/server/calculator/domain/operator';

it('performsAddition', () => {
  const calculation = Calculation.perform(CalculationId.generate(), 2, Operator.ADD, 3);

  expect(calculation.result).toBe(5);

  const events = calculation.popEvents();
  expect(events).toHaveLength(1);
  expect(events[0]).toBeInstanceOf(CalculationPerformed);
  const event = events[0] as CalculationPerformed;
  expect(event.calculationId).toEqual(calculation.id);
  expect(event.result).toBe(5);
  expect(calculation.popEvents()).toEqual([]);
});

it('divideByZeroThrows', () => {
  expect(() => Calculation.perform(CalculationId.generate(), 1, Operator.DIVIDE, 0))
    .toThrow(DomainRuleViolation);
});
