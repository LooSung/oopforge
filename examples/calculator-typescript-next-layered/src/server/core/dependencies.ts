import 'server-only';

import { InMemoryCalculationRepository } from '../calculator/repository/inMemoryCalculationRepository';
import { CalculatorService } from '../calculator/service/calculatorService';

export const calculatorService: CalculatorService = new CalculatorService(new InMemoryCalculationRepository());
