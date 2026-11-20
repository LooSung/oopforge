'use server';

import { calculatorConfig } from '../../config/calculatorConfig';
import type { CalculateActionResult } from './calculateActionResult';
import { parseCalculateRequest } from './calculateRequest';
import { toCalculationResponse } from './calculationResponse';
import { NormalizedRequest } from './normalizedRequest';
import { safeError } from './webErrorHandler';

// The second inbound adapter. A server action is internal RPC, so it stays out
// of the OpenAPI document, but it is still a public POST endpoint: its input is
// untrusted and goes through the same zod schema as the route handler.
export async function calculateAction(input: unknown): Promise<CalculateActionResult> {
  try {
    const request = NormalizedRequest.from(parseCalculateRequest(input));
    const result = await calculatorConfig().calculate.handle(request.toCommand());
    return { ok: true, calculation: toCalculationResponse(result) };
  } catch (error) {
    return { ok: false, error: safeError(error).body };
  }
}
