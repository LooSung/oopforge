import { Injectable } from '@nestjs/common';

import { Calculation } from '../../domain/calculation.js';
import { CalculationId } from '../../domain/calculation-id.js';
import { Calculate, type CalculateCommand, type CalculationResult } from '../provided/calculate.js';
import { CalculationRepository } from '../required/calculation.repository.js';
import { DomainEventDispatcher } from '../required/domain-event-dispatcher.js';
import { TransactionRunner } from '../required/transaction-runner.js';

// The ports are value imports, not `import type`: Nest reads them from the
// constructor's decorator metadata as injection tokens.
@Injectable()
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
