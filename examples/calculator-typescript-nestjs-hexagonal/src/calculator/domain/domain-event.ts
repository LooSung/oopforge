export abstract class DomainEvent {
  readonly eventId: string = crypto.randomUUID();
  private readonly occurredAtEpochMillis: number = Date.now();

  // A Date is mutable, so callers get a copy, never the event's own instant.
  get occurredAt(): Date {
    return new Date(this.occurredAtEpochMillis);
  }
}
