import type { CalculatorConfig } from '../../config/calculatorConfig';
import { calculatorConfig } from '../../config/calculatorConfig';
import { parseCalculateRequest } from './calculateRequest';
import type { RouteHandler } from './correlationAuditFilter';
import { withCorrelationAudit } from './correlationAuditFilter';
import type { IdempotentCalculationHandler } from './idempotentCalculationHandler';
import { IDEMPOTENCY_KEY_HEADER } from './idempotencyStore';
import { InvalidWebRequestError } from './invalidWebRequestError';
import { withWebErrorHandling } from './webErrorHandler';

const CALCULATION_CREATE = 'calculation.create';

export function createCalculatorController(config: CalculatorConfig): RouteHandler {
  const handle = withWebErrorHandling((request) => calculate(request, config.calculationHandler));
  return withCorrelationAudit(handle, { audit: config.audit, action: CALCULATION_CREATE });
}

// POST /calculations, re-exported by src/app/calculations/route.ts. Only the
// entry modules (this one and calculateAction) reach the composition root;
// everything below them receives collaborators through constructors.
export const POST: RouteHandler = createCalculatorController(calculatorConfig());

async function calculate(request: Request, handler: IdempotentCalculationHandler): Promise<Response> {
  const body = parseCalculateRequest(await request.json().catch(rejectMalformedJson));
  const response = await handler.handle(body, request.headers.get(IDEMPOTENCY_KEY_HEADER));
  return Response.json(response, { status: 201 });
}

function rejectMalformedJson(): never {
  throw new InvalidWebRequestError();
}
