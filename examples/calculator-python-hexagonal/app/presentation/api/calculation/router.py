from fastapi import APIRouter, Depends, status

from app.application.services.calculation.calculate_service import (
    CalculateCommand,
    CalculateService,
)
from app.core.dependencies import get_calculate_service
from app.presentation.api.calculation.request import CalculateRequest, CalculationResponse

_router = APIRouter(prefix="/calculations", tags=["calculations"])


@_router.post("", response_model=CalculationResponse, status_code=status.HTTP_201_CREATED)
def calculate(
    body: CalculateRequest,
    service: CalculateService = Depends(get_calculate_service),
) -> CalculationResponse:
    result = service.handle(
        CalculateCommand(operand_a=body.operand_a, operator=body.operator, operand_b=body.operand_b)
    )
    return CalculationResponse(
        calculation_id=result.calculation_id,
        operand_a=result.operand_a,
        operator=result.operator,
        operand_b=result.operand_b,
        result=result.result,
    )


router = _router
