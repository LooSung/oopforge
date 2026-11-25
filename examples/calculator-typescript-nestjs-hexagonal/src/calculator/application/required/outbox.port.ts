import type { OutboxMessage } from './outbox-message.js';

export abstract class OutboxPort {
  abstract append(message: OutboxMessage): Promise<void>;

  abstract unpublished(): Promise<ReadonlyArray<OutboxMessage>>;

  abstract markPublished(messageId: string, publishedAt: Date): Promise<void>;

  abstract publishedAt(messageId: string): Promise<Date | undefined>;
}
