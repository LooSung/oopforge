import { z } from 'zod';

import type { HistorySummary } from '../../application/query/historySummary';

export const HistoryEntryResponse = z
  .object({
    calculationId: z.string(),
    operandA: z.number(),
    operandB: z.number(),
    operator: z.string(),
    result: z.number(),
    performedAt: z.iso.datetime(),
  })
  .meta({ id: 'HistoryEntryResponse' });

export type HistoryEntryResponse = z.infer<typeof HistoryEntryResponse>;

export function toHistoryEntryResponse(summary: HistorySummary): HistoryEntryResponse {
  return {
    calculationId: summary.calculationId,
    operandA: summary.operandA,
    operandB: summary.operandB,
    operator: summary.operator,
    result: summary.result,
    performedAt: summary.performedAt,
  };
}
