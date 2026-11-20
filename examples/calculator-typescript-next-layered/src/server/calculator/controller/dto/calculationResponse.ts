import { z } from 'zod';

export const CalculationResponse = z
  .object({
    calculationId: z.string(),
    operandA: z.number(),
    operator: z.string(),
    operandB: z.number(),
    result: z.number(),
  })
  .meta({ id: 'CalculationResponse' });

export type CalculationResponse = z.infer<typeof CalculationResponse>;
