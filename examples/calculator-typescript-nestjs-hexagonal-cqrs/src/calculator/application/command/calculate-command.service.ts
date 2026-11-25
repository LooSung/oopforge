import { Injectable } from '@nestjs/common';

import { Calculation } from '../../domain/calculation.js';
import { CalculationId } from '../../domain/calculation-id.js';
import { Calculate, type CalculateCommand } from './calculate.js';
import { CalculationRepository } from './calculation.repository.js';

@Injectable()
export class CalculateCommandService extends Calculate {
  constructor(private readonly calculationRepository: CalculationRepository) {
    super();
  }

  async handle(command: CalculateCommand): Promise<CalculationId> {
    const id = CalculationId.generate();
    const calculation = Calculation.perform(id, command.operandA, command.operator, command.operandB);
    await this.calculationRepository.save(calculation);
    return id;
  }
}
