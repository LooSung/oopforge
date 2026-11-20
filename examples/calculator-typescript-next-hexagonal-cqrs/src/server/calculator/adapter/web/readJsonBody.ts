import type { z } from 'zod';

import { badRequest } from './badRequest';

export type JsonBody<T> =
  | { readonly ok: true; readonly value: T }
  | { readonly ok: false; readonly response: Response };

export async function readJsonBody<T>(request: Request, schema: z.ZodType<T>): Promise<JsonBody<T>> {
  let raw: unknown;
  try {
    raw = await request.json();
  } catch {
    return { ok: false, response: badRequest(request, 'Malformed JSON request body') };
  }
  const parsed = schema.safeParse(raw);
  if (!parsed.success) {
    return { ok: false, response: badRequest(request, 'Request body failed validation') };
  }
  return { ok: true, value: parsed.data };
}
