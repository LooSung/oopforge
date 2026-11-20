import type { ApiError } from './apiError';
import type { CalculationResponse } from './calculationResponse';

// A 'use server' module may export only async functions, so the action's
// result type lives here. Expected failures come back as data, not throws:
// Next.js redacts thrown errors before they reach the caller.
export type CalculateActionResult =
  | { readonly ok: true; readonly calculation: CalculationResponse }
  | { readonly ok: false; readonly error: ApiError };
