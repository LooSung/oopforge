import { z } from 'zod';

import { HistoryEntryResponse } from './historyEntryResponse';

export const HistoryListResponse = z
  .object({ items: z.array(HistoryEntryResponse) })
  .meta({ id: 'HistoryListResponse' });

export type HistoryListResponse = z.infer<typeof HistoryListResponse>;
