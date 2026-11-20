import type { DomainEvent } from '../../domain/domainEvent';

export type DomainEventType<T extends DomainEvent> = abstract new (...args: never[]) => T;

export interface DomainEventHandler<T extends DomainEvent> {
  readonly eventType: DomainEventType<T>;
  handle(event: T): Promise<void>;
}
