import { expect, it } from 'vitest';
import { calculateAction } from '../../../../../src/server/calculator/adapter/web/calculateAction';
import { calculatorConfig } from '../../../../../src/server/calculator/config/calculatorConfig';

// TypeScript addition: the server action is the second inbound adapter. It is
// called directly, the way a Server Component or form would call it.
it('performsTheCalculationThroughTheSameApplicationService', async () => {
  const initialOutboxRows = (await calculatorConfig().outbox.unpublished()).length;

  const result = await calculateAction({ operandA: 6, operator: 'DIVIDE', operandB: 2 });

  expect(result).toMatchObject({
    ok: true,
    calculation: { operandA: 6, operator: 'divide', operandB: 2, result: 3 },
  });
  expect(await calculatorConfig().outbox.unpublished()).toHaveLength(initialOutboxRows + 1);
});

it('rejectsInvalidInputWithTheSameSafeError', async () => {
  const result = await calculateAction({ operandA: 1, operandB: 2 });

  expect(result).toEqual({
    ok: false,
    error: { code: 'invalid_request', message: 'The request is invalid.' },
  });
});

it('returnsASafeDomainErrorForDivisionByZero', async () => {
  const result = await calculateAction({ operandA: 1, operator: 'DIVIDE', operandB: 0 });

  expect(result).toEqual({
    ok: false,
    error: { code: 'calculation_rejected', message: 'The calculation could not be performed.' },
  });
});
