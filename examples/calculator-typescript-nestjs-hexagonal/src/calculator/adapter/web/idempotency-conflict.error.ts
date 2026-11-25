export class IdempotencyConflictError extends Error {
  override readonly name = 'IdempotencyConflictError';
}
