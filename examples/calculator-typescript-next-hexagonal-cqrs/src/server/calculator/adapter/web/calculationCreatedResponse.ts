import { z } from 'zod';

export const CalculationCreatedResponse = z
  .object({ calculationId: z.string() })
  .meta({ id: 'CalculationCreatedResponse' });

export type CalculationCreatedResponse = z.infer<typeof CalculationCreatedResponse>;
