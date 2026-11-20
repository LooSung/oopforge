import type { DomainEvent } from '../../domain/domainEvent';

export interface DomainEventDispatcher {
  dispatch(events: ReadonlyArray<DomainEvent>): Promise<void>;
}
