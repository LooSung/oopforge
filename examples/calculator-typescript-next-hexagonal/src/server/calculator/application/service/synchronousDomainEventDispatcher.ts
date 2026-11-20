import type { DomainEvent } from '../../domain/domainEvent';
import type { DomainEventDispatcher } from '../required/domainEventDispatcher';
import type { DomainEventHandler } from './domainEventHandler';

// "Synchronous" means in-process and inside the caller's transaction: handlers
// are awaited one by one, so the first failure rolls the whole unit back.
export class SynchronousDomainEventDispatcher implements DomainEventDispatcher {
  private readonly handlers: ReadonlyArray<DomainEventHandler<DomainEvent>>;

  constructor(handlers: ReadonlyArray<DomainEventHandler<DomainEvent>>) {
    this.handlers = [...handlers];
  }

  async dispatch(events: ReadonlyArray<DomainEvent>): Promise<void> {
    for (const event of events) {
      await this.dispatchEvent(event);
    }
  }

  private async dispatchEvent(event: DomainEvent): Promise<void> {
    for (const handler of this.handlers) {
      if (event instanceof handler.eventType) {
        await handler.handle(event);
      }
    }
  }
}
