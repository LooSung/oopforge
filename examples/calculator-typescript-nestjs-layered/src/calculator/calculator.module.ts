import { Module } from '@nestjs/common';

import { CalculatorController } from './controller/calculator.controller.js';
import { CalculationRepository } from './repository/calculation.repository.js';
import { InMemoryCalculationRepository } from './repository/in-memory-calculation.repository.js';
import { CalculatorService } from './service/calculator.service.js';

// Composition: the only file that names every layer.
@Module({
  controllers: [CalculatorController],
  providers: [
    CalculatorService,
    { provide: CalculationRepository, useClass: InMemoryCalculationRepository },
  ],
})
export class CalculatorModule {}
