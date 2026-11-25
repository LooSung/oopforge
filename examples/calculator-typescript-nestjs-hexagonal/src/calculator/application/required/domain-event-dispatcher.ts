import type { DomainEvent } from '../../domain/domain-event.js';

export abstract class DomainEventDispatcher {
  abstract dispatch(events: ReadonlyArray<DomainEvent>): Promise<void>;
}
