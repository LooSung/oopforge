import { z } from 'zod';

export const HistoryQueryParams = z.object({
  limit: z.coerce.number().int().positive().default(20),
});

export type HistoryQueryParams = z.infer<typeof HistoryQueryParams>;
