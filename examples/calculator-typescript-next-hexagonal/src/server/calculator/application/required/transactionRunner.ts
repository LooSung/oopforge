// The transaction boundary is an explicit unit-of-work port: TypeScript has no
// framework annotation, so the application service opens it itself.
export interface TransactionRunner {
  run<T>(work: () => Promise<T>): Promise<T>;
}
