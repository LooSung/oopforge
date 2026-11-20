import { calculatorService } from '../../core/dependencies';
import { Operator } from '../domain/operator';
import type { CalculationResult } from '../service/calculatorService';
import { CalculateRequest } from './dto/calculateRequest';
import type { CalculationResponse } from './dto/calculationResponse';
import { readJsonBody } from './readJsonBody';

export async function POST(request: Request): Promise<Response> {
  const body = await readJsonBody(request, CalculateRequest);
  if (!body.ok) {
    return body.response;
  }
  const result = calculatorService.calculate({
    operandA: body.value.operandA,
    operator: Operator.of(body.value.operator),
    operandB: body.value.operandB,
  });
  return Response.json(toResponse(result), { status: 201 });
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
