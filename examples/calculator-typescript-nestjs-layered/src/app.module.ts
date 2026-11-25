import { Module } from '@nestjs/common';

import { CalculatorModule } from './calculator/calculator.module.js';

@Module({ imports: [CalculatorModule] })
export class AppModule {}
