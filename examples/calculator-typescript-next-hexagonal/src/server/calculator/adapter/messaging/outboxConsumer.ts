import type { OutboxMessage } from '../../application/required/outboxMessage';

export interface OutboxConsumer {
  consume(message: OutboxMessage): Promise<void>;
}
