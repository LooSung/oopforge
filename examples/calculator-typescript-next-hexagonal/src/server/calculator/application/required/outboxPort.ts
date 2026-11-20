import type { OutboxMessage } from './outboxMessage';

export interface OutboxPort {
  append(message: OutboxMessage): Promise<void>;
  unpublished(): Promise<ReadonlyArray<OutboxMessage>>;
  markPublished(messageId: string, publishedAt: Date): Promise<void>;
  publishedAt(messageId: string): Promise<Date | undefined>;
}
