import { z } from 'zod';

export const apiErrorSchema = z
  .object({
    code: z.string(),
    message: z.string(),
  })
  .meta({ id: 'ApiError' });

export type ApiError = z.infer<typeof apiErrorSchema>;
