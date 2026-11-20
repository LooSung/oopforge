import { calculatorConfig } from '../../config/calculatorConfig';
import { Operator } from '../../domain/operator';
import { CalculateRequest } from './calculateRequest';
import type { CalculationCreatedResponse } from './calculationCreatedResponse';
import { readJsonBody } from './readJsonBody';

export async function calculate(request: Request): Promise<Response> {
  const body = await readJsonBody(request, CalculateRequest);
  if (!body.ok) {
    return body.response;
  }
  const id = calculatorConfig.calculate.handle({
    operandA: body.value.operandA,
    operator: Operator.of(body.value.operator),
    operandB: body.value.operandB,
  });
  const created: CalculationCreatedResponse = { calculationId: id.value };
  return Response.json(created, { status: 201 });
}
