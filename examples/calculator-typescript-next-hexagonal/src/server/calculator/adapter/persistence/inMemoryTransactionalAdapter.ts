import { AsyncLocalStorage } from 'node:async_hooks';
import type { CalculationRepository } from '../../application/required/calculationRepository';
import type { OutboxMessage } from '../../application/required/outboxMessage';
import type { OutboxPort } from '../../application/required/outboxPort';
import type { TransactionRunner } from '../../application/required/transactionRunner';
import type { Calculation } from '../../domain/calculation';
import type { CalculationId } from '../../domain/calculationId';

interface OutboxRow {
  readonly message: OutboxMessage;
  readonly publishedAtEpochMillis: number | undefined;
}

interface TransactionState {
  readonly calculations: Map<string, Calculation>;
  readonly messages: OutboxMessage[];
}

// Maps are keyed by the id's string value: JavaScript compares object keys by
// identity, so a CalculationId key would never be found again. No method body
// awaits, so no other request can interleave inside one: Java's `synchronized`
// has nothing to protect here.
export class InMemoryTransactionalAdapter implements CalculationRepository, OutboxPort, TransactionRunner {
  private readonly calculations = new Map<string, Calculation>();
  private readonly outbox = new Map<string, OutboxRow>();
  // The async counterpart of Java's ThreadLocal: concurrent requests interleave
  // at every await, so each keeps its own transaction state.
  private readonly transactions = new AsyncLocalStorage<TransactionState>();

  async run<T>(work: () => Promise<T>): Promise<T> {
    if (this.transactions.getStore() !== undefined) {
      throw new Error('nested transactions are not supported');
    }
    const transaction: TransactionState = { calculations: new Map(), messages: [] };
    const result = await this.transactions.run(transaction, work);
    this.commit(transaction);
    return result;
  }

  async save(calculation: Calculation): Promise<void> {
    this.activeTransaction().calculations.set(calculation.id.value, calculation);
  }

  async findById(id: CalculationId): Promise<Calculation | undefined> {
    const pending = this.transactions.getStore()?.calculations.get(id.value);
    return pending ?? this.calculations.get(id.value);
  }

  async append(message: OutboxMessage): Promise<void> {
    this.activeTransaction().messages.push(message);
  }

  async unpublished(): Promise<ReadonlyArray<OutboxMessage>> {
    return [...this.outbox.values()]
      .filter((row) => row.publishedAtEpochMillis === undefined)
      .map((row) => row.message);
  }

  async markPublished(messageId: string, publishedAt: Date): Promise<void> {
    const row = this.outbox.get(messageId);
    if (row === undefined) {
      throw new Error('unknown outbox message');
    }
    this.outbox.set(messageId, { message: row.message, publishedAtEpochMillis: publishedAt.getTime() });
  }

  async publishedAt(messageId: string): Promise<Date | undefined> {
    const publishedAt = this.outbox.get(messageId)?.publishedAtEpochMillis;
    return publishedAt === undefined ? undefined : new Date(publishedAt);
  }

  private activeTransaction(): TransactionState {
    const transaction = this.transactions.getStore();
    if (transaction === undefined) {
      throw new Error('operation requires an active transaction');
    }
    return transaction;
  }

  // Runs without awaiting, so the calculation and its outbox rows land together.
  private commit(transaction: TransactionState): void {
    transaction.calculations.forEach((calculation, id) => this.calculations.set(id, calculation));
    transaction.messages.forEach((message) => {
      this.outbox.set(message.id, { message, publishedAtEpochMillis: undefined });
    });
  }
}
