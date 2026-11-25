import { Injectable } from '@nestjs/common';

import { OutboxPort } from '../../application/required/outbox.port.js';
import { OutboxConsumer } from './outbox-consumer.js';

@Injectable()
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
