import type { OutboxMessage } from '../../application/required/outbox-message.js';

// An abstract class so the relay can receive its consumer by injection.
export abstract class OutboxConsumer {
  abstract consume(message: OutboxMessage): Promise<void>;
}
