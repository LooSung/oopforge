import { Injectable } from '@nestjs/common';

import type { CalculationResponse } from './calculation.response.js';
import { IdempotencyConflictError } from './idempotency-conflict.error.js';
import { InvalidWebRequestError } from './invalid-web-request.error.js';
import type { NormalizedRequest } from './normalized-request.js';

export const IDEMPOTENCY_KEY_HEADER = 'Idempotency-Key';

export const MAX_KEY_LENGTH = 200;

interface StoredResult {
  readonly request: NormalizedRequest;
  readonly response: CalculationResponse;
}

@Injectable()
export class IdempotencyStore {
  private readonly results = new Map<string, StoredResult>();
  private readonly keyQueues = new Map<string, Promise<void>>();

  async execute(
    key: string | null,
    request: NormalizedRequest,
    operation: () => Promise<CalculationResponse>,
  ): Promise<CalculationResponse> {
    if (key === null) {
      return operation();
    }
    validate(key);
    return this.withKeyLock(key, () => this.executeLocked(key, request, operation));
  }

  private async executeLocked(
    key: string,
    request: NormalizedRequest,
    operation: () => Promise<CalculationResponse>,
  ): Promise<CalculationResponse> {
    const stored = this.results.get(key);
    if (stored === undefined) {
      const response = await operation();
      this.results.set(key, { request, response });
      return response;
    }
    if (!stored.request.equals(request)) {
      throw new IdempotencyConflictError();
    }
    return stored.response;
  }

  // The port of Java's per-key `synchronized`: check-then-act spans an await,
  // so a same-key request waits for the previous one. A failed operation stores
  // nothing and still releases the key for the next caller.
  private async withKeyLock<T>(key: string, work: () => Promise<T>): Promise<T> {
    const previous = this.keyQueues.get(key) ?? Promise.resolve();
    const current = previous.then(work);
    const settled = current.then(() => undefined, () => undefined);
    this.keyQueues.set(key, settled);
    try {
      return await current;
    } finally {
      if (this.keyQueues.get(key) === settled) {
        this.keyQueues.delete(key);
      }
    }
  }
}

function validate(key: string): void {
  if (key.trim() === '' || key.length > MAX_KEY_LENGTH) {
    throw new InvalidWebRequestError();
  }
}
