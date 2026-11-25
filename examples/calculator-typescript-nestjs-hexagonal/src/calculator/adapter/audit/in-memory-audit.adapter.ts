import { Injectable, Logger } from '@nestjs/common';

export interface AuditEntry {
  readonly correlationId: string;
  readonly action: string;
  readonly outcome: string;
}

@Injectable()
export class InMemoryAuditAdapter {
  private readonly logger = new Logger('Audit');
  private readonly recorded: AuditEntry[] = [];

  record(correlationId: string, action: string, outcome: string): void {
    const entry: AuditEntry = Object.freeze({ correlationId, action, outcome });
    this.recorded.push(entry);
    this.logger.log(`correlationId=${entry.correlationId} action=${entry.action} outcome=${entry.outcome}`);
  }

  entries(): ReadonlyArray<AuditEntry> {
    return [...this.recorded];
  }
}
