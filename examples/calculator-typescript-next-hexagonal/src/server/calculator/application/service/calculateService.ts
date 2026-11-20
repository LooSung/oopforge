import { Calculation } from '../../domain/calculation';
import { CalculationId } from '../../domain/calculationId';
import type { Calculate, CalculateCommand, CalculationResult } from '../provided/calculate';
import type { CalculationRepository } from '../required/calculationRepository';
import type { DomainEventDispatcher } from '../required/domainEventDispatcher';
import type { TransactionRunner } from '../required/transactionRunner';

export class CalculateService implements Calculate {
  constructor(
    private readonly calculationRepository: CalculationRepository,
    private readonly transactionRunner: TransactionRunner,
    private readonly eventDispatcher: DomainEventDispatcher,
  ) {}

  async handle(command: CalculateCommand): Promise<CalculationResult> {
    return this.transactionRunner.run(() => this.calculate(command));
  }

  private async calculate(command: CalculateCommand): Promise<CalculationResult> {
    const id = CalculationId.generate();
    const calculation = Calculation.perform(id, command.operandA, command.operator, command.operandB);
    await this.calculationRepository.save(calculation);
    await this.eventDispatcher.dispatch(calculation.popEvents());
    return {
      calculationId: id.value,
      operandA: calculation.operandA,
      operator: calculation.operator,
      operandB: calculation.operandB,
      result: calculation.result,
    };
  }
}
