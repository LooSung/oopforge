from fastapi import APIRouter, Depends, status

from app.calculator.schemas.api_models import CalculateRequest, CalculationResponse
from app.calculator.service.calculator_service import CalculatorService
from app.core.dependencies import get_calculator_service

router = APIRouter(prefix="/api/v1/calculations", tags=["Calculator"])


@router.post("", response_model=CalculationResponse, status_code=status.HTTP_201_CREATED)
def calculate(
    body: CalculateRequest,
    service: CalculatorService = Depends(get_calculator_service),
) -> CalculationResponse:
    result = service.calculate(body.operand_a, body.operator, body.operand_b)
    return CalculationResponse(
        calculation_id=result.calculation_id,
        operand_a=result.operand_a,
        operator=result.operator,
        operand_b=result.operand_b,
        result=result.result,
    )
