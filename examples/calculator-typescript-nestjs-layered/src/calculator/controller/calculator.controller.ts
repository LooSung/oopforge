import { Body, Controller, Post } from '@nestjs/common';
import { ApiBadRequestResponse, ApiCreatedResponse, ApiTags } from '@nestjs/swagger';

import { Operator } from '../domain/operator.js';
import { CalculatorService, type CalculationResult } from '../service/calculator.service.js';
import { calculateRequest, type CalculateRequest } from './calculate.request.js';
import type { CalculationResponse } from './calculation.response.js';

@ApiTags('Calculator')
@Controller('api/v1/calculations')
export class CalculatorController {
  constructor(private readonly calculatorService: CalculatorService) {}

  @Post()
  @ApiCreatedResponse({ description: 'Created' })
  @ApiBadRequestResponse({ description: 'Malformed JSON or a body that fails validation' })
  async calculate(@Body({ schema: calculateRequest }) body: CalculateRequest): Promise<CalculationResponse> {
    const result = await this.calculatorService.calculate({
      operandA: body.operandA,
      operator: Operator.of(body.operator),
      operandB: body.operandB,
    });
    return toResponse(result);
  }
}

function toResponse(result: CalculationResult): CalculationResponse {
  return {
    calculationId: result.calculationId,
    operandA: result.operandA,
    operator: result.operator.name.toLowerCase(),
    operandB: result.operandB,
    result: result.result,
  };
}
