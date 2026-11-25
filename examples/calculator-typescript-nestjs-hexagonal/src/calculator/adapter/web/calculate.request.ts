import { z } from 'zod';

import { OPERATOR_NAMES } from '../../domain/operator.js';

// zod 4's z.number() rejects NaN and ±Infinity, which covers Java's
// @AssertTrue "operands must be finite". Unknown keys are stripped, as with
// Spring's default Jackson setup, so extra fields never reach the use case.
export const calculateRequestSchema = z
  .object({
    operandA: z.number().meta({ example: 8 }),
    operator: z.enum(OPERATOR_NAMES),
    operandB: z.number().meta({ example: 2 }),
  })
  .meta({ id: 'CalculateRequest' });

export type CalculateRequest = z.infer<typeof calculateRequestSchema>;
