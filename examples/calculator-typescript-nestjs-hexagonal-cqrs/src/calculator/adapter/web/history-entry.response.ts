import type { HistorySummary } from '../../application/query/history-summary.js';

export interface HistoryEntryResponse {
  readonly calculationId: string;
  readonly operandA: number;
  readonly operandB: number;
  readonly operator: string;
  readonly result: number;
  readonly performedAt: string;
}

export interface HistoryListResponse {
  readonly items: ReadonlyArray<HistoryEntryResponse>;
}

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
