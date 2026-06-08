from fastapi import APIRouter, Depends, status

from app.application.command.calculate_command_service import CalculateCommandService
from app.core.dependencies import get_command_service
from app.presentation.api.schemas import CalculateRequest, CalculationCreatedResponse

router = APIRouter(prefix="/api/v1/calculations", tags=["Calculator Commands"])


@router.post("", response_model=CalculationCreatedResponse, status_code=status.HTTP_201_CREATED)
def calculate(
    body: CalculateRequest,
    service: CalculateCommandService = Depends(get_command_service),
) -> CalculationCreatedResponse:
    calculation_id = service.calculate(body.operand_a, body.operator, body.operand_b)
    return CalculationCreatedResponse(calculation_id=str(calculation_id.value))
