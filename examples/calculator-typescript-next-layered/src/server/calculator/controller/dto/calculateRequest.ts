import { z } from 'zod';

import { OPERATOR_NAMES } from '../../domain/operator';

export const CalculateRequest = z
  .object({
    operandA: z.number(),
    operator: z.enum(OPERATOR_NAMES),
    operandB: z.number(),
  })
  .meta({ id: 'CalculateRequest' });

export type CalculateRequest = z.infer<typeof CalculateRequest>;
