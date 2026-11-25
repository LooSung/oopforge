import { Module } from '@nestjs/common';

import { CalculationStore } from './adapter/persistence/calculation-store.js';
import { InMemoryCalculationRepository } from './adapter/persistence/in-memory-calculation.repository.js';
import { InMemoryHistoryQueryRepository } from './adapter/persistence/in-memory-history-query.repository.js';
import { CalculatorCommandController } from './adapter/web/calculator-command.controller.js';
import { CalculatorQueryController } from './adapter/web/calculator-query.controller.js';
import { Calculate } from './application/command/calculate.js';
import { CalculateCommandService } from './application/command/calculate-command.service.js';
import { CalculationRepository } from './application/command/calculation.repository.js';
import { CalculationHistory } from './application/query/calculation-history.js';
import { HistoryQueryRepository } from './application/query/history-query.repository.js';
import { HistoryQueryService } from './application/query/history-query.service.js';

// Composition: binds each port to its adapter or service. CalculationStore is a
// singleton provider, so the write and read adapters share it.
@Module({
  controllers: [CalculatorCommandController, CalculatorQueryController],
  providers: [
    CalculationStore,
    { provide: CalculationRepository, useClass: InMemoryCalculationRepository },
    { provide: HistoryQueryRepository, useClass: InMemoryHistoryQueryRepository },
    { provide: Calculate, useClass: CalculateCommandService },
    { provide: CalculationHistory, useClass: HistoryQueryService },
  ],
})
export class CalculatorModule {}
