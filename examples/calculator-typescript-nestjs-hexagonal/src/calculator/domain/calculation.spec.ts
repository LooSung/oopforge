import { Calculation } from './calculation.js';
import { CalculationId } from './calculation-id.js';
import { CalculationPerformed } from './calculation-performed.js';
import { DomainRuleViolation } from './domain-rule-violation.js';
import { Operator } from './operator.js';

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
