import { z } from 'zod';

export const calculationIdParam = z.guid();

export const historyLimitQuery = z.coerce.number().int().positive().default(20);
