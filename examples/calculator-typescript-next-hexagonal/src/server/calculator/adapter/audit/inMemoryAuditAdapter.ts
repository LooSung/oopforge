export interface AuditEntry {
  readonly correlationId: string;
  readonly action: string;
  readonly outcome: string;
}

export class InMemoryAuditAdapter {
  private readonly recorded: AuditEntry[] = [];

  record(correlationId: string, action: string, outcome: string): void {
    const entry: AuditEntry = Object.freeze({ correlationId, action, outcome });
    this.recorded.push(entry);
    console.info(
      `audit correlationId=${entry.correlationId} action=${entry.action} outcome=${entry.outcome}`,
    );
  }

  entries(): ReadonlyArray<AuditEntry> {
    return [...this.recorded];
  }
}
