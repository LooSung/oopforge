import { calculatorConfig } from '../../config/calculatorConfig';
import { CalculationId } from '../../domain/calculationId';
import { badRequest } from './badRequest';
import { CalculationPathParams } from './calculationPathParams';
import { toHistoryEntryResponse } from './historyEntryResponse';
import type { HistoryListResponse } from './historyListResponse';
import { HistoryQueryParams } from './historyQueryParams';

export interface CalculationRouteContext {
  readonly params: Promise<{ calculationId: string }>;
}

export async function listHistory(request: Request): Promise<Response> {
  const query = HistoryQueryParams.safeParse(Object.fromEntries(new URL(request.url).searchParams));
  if (!query.success) {
    return badRequest(request, 'limit must be a positive integer');
  }
  const summaries = await calculatorConfig.calculationHistory.listRecent(query.data.limit);
  const body: HistoryListResponse = { items: summaries.map(toHistoryEntryResponse) };
  return Response.json(body);
}

export async function getCalculation(request: Request, context: CalculationRouteContext): Promise<Response> {
  const params = CalculationPathParams.safeParse(await context.params);
  if (!params.success) {
    return badRequest(request, 'calculationId must be a UUID');
  }
  const id = CalculationId.of(params.data.calculationId);
  const summary = await calculatorConfig.calculationHistory.findById(id);
  if (summary === undefined) {
    return new Response(null, { status: 404 });
  }
  return Response.json(toHistoryEntryResponse(summary));
}
