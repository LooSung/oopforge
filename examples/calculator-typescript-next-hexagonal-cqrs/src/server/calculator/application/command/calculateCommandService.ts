import { Calculation } from '../../domain/calculation';
import { CalculationId } from '../../domain/calculationId';
import type { Calculate, CalculateCommand } from './calculate';
import type { CalculationRepository } from './calculationRepository';

export class CalculateCommandService implements Calculate {
  constructor(private readonly calculationRepository: CalculationRepository) {}

  async handle(command: CalculateCommand): Promise<CalculationId> {
    const id = CalculationId.generate();
    const calculation = Calculation.perform(id, command.operandA, command.operator, command.operandB);
    await this.calculationRepository.save(calculation);
    return id;
  }
}
