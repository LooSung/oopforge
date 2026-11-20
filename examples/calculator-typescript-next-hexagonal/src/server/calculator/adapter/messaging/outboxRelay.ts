import type { OutboxPort } from '../../application/required/outboxPort';
import type { OutboxConsumer } from './outboxConsumer';

export class OutboxRelay {
  constructor(
    private readonly outbox: OutboxPort,
    private readonly consumer: OutboxConsumer,
  ) {}

  async relay(): Promise<void> {
    for (const message of await this.outbox.unpublished()) {
      await this.consumer.consume(message);
      await this.outbox.markPublished(message.id, new Date());
    }
  }
}
