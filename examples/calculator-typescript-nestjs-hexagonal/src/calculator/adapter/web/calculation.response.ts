import { z } from 'zod';

import type { CalculationResult } from '../../application/provided/calculate.js';

export const calculationResponseSchema = z
  .object({
    calculationId: z.uuid(),
    operandA: z.number(),
    operator: z.string().meta({ example: 'divide' }),
    operandB: z.number(),
    result: z.number(),
  })
  .meta({ id: 'CalculationResponse' });

export type CalculationResponse = z.infer<typeof calculationResponseSchema>;

export function toCalculationResponse(result: CalculationResult): CalculationResponse {
  return Object.freeze({
    calculationId: result.calculationId,
    operandA: result.operandA,
    operator: result.operator.name.toLowerCase(),
    operandB: result.operandB,
    result: result.result,
  });
}
