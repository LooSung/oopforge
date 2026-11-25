export interface OutboxMessage {
  readonly id: string;
  readonly aggregateId: string;
  readonly eventType: string;
  readonly payload: unknown;
  // ISO-8601: a Date inside a shared record could be mutated by any reader.
  readonly occurredAt: string;
}

export function outboxMessage(fields: OutboxMessage): OutboxMessage {
  return Object.freeze({ ...fields });
}
