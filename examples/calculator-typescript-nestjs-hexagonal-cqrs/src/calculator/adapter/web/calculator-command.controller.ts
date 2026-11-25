import { Body, Controller, Post } from '@nestjs/common';
import { ApiBadRequestResponse, ApiCreatedResponse, ApiTags } from '@nestjs/swagger';

import { Calculate } from '../../application/command/calculate.js';
import { Operator } from '../../domain/operator.js';
import { calculateRequest, type CalculateRequest } from './calculate.request.js';
import type { CalculationCreatedResponse } from './calculation-created.response.js';

@ApiTags('Calculator Commands')
@Controller('api/v1/calculations')
export class CalculatorCommandController {
  constructor(private readonly calculateUseCase: Calculate) {}

  @Post()
  @ApiCreatedResponse({ description: 'Created; the body holds only calculationId' })
  @ApiBadRequestResponse({ description: 'Malformed JSON or a body that fails validation' })
  async calculate(@Body({ schema: calculateRequest }) body: CalculateRequest): Promise<CalculationCreatedResponse> {
    const id = await this.calculateUseCase.handle({
      operandA: body.operandA,
      operator: Operator.of(body.operator),
      operandB: body.operandB,
    });
    return { calculationId: id.value };
  }
}
