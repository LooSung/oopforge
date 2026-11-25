// The transaction boundary is an explicit unit-of-work port: Nest has no
// transaction annotation, so the application service opens it itself.
export abstract class TransactionRunner {
  abstract run<T>(work: () => Promise<T>): Promise<T>;
}
