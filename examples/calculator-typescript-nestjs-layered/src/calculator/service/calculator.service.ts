import { Injectable } from '@nestjs/common';

import { Calculation } from '../domain/calculation.js';
import { CalculationId } from '../domain/calculation-id.js';
import type { Operator } from '../domain/operator.js';
import { CalculationRepository } from '../repository/calculation.repository.js';

export interface CalculateCommand {
  readonly operandA: number;
  readonly operator: Operator;
  readonly operandB: number;
}

export interface CalculationResult {
  readonly calculationId: string;
  readonly operandA: number;
  readonly operator: Operator;
  readonly operandB: number;
  readonly result: number;
}

@Injectable()
export class CalculatorService {
  constructor(private readonly calculationRepository: CalculationRepository) {}

  async calculate(command: CalculateCommand): Promise<CalculationResult> {
    const id = CalculationId.generate();
    const calculation = Calculation.perform(id, command.operandA, command.operator, command.operandB);
    await this.calculationRepository.save(calculation);
    return {
      calculationId: id.value,
      operandA: calculation.operandA,
      operator: calculation.operator,
      operandB: calculation.operandB,
      result: calculation.result,
    };
  }
}
