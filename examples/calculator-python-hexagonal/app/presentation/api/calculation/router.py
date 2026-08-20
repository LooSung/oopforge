from typing import Annotated

from fastapi import APIRouter, Depends, Header, status

from app.application.services.calculation.calculate_service import CalculateService
from app.core.dependencies import get_calculate_service, get_idempotency_store
from app.presentation.api.calculation.handler import CalculationHttpHandler
from app.presentation.api.calculation.request import CalculateRequest, CalculationResponse
from app.presentation.api.idempotency import IdempotencyStore

_router = APIRouter(prefix="/calculations", tags=["calculations"])


@_router.post("", response_model=CalculationResponse, status_code=status.HTTP_201_CREATED)
def calculate(
    body: CalculateRequest,
    idempotency_key: Annotated[str | None, Header(alias="Idempotency-Key")] = None,
    service: CalculateService = Depends(get_calculate_service),
    idempotency_store: IdempotencyStore = Depends(get_idempotency_store),
) -> CalculationResponse:
    return CalculationHttpHandler(service, idempotency_store).handle(
        body,
        idempotency_key,
    )


router = _router
