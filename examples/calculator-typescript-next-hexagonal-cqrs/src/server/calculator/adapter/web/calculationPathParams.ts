import { z } from 'zod';

export const CalculationPathParams = z.object({
  calculationId: z.guid(),
});

export type CalculationPathParams = z.infer<typeof CalculationPathParams>;
