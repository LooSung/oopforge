from app.application.services.calculation.calculate_service import (
    CalculateCommand,
    CalculateService,
)
from app.presentation.api.calculation.request import (
    CalculateRequest,
    CalculationResponse,
)
from app.presentation.api.errors import DomainCalculationError
from app.presentation.api.idempotency import (
    IdempotencyStore,
    normalize_idempotency_key,
)
from app.presentation.api.observability import mark_outcome


class CalculationHttpHandler:
    def __init__(
        self,
        service: CalculateService,
        idempotency_store: IdempotencyStore,
    ) -> None:
        self._service = service
        self._idempotency_store = idempotency_store

    def handle(
        self,
        request: CalculateRequest,
        idempotency_key: str | None,
    ) -> CalculationResponse:
        if idempotency_key is None:
            response = self._calculate(request)
            mark_outcome("created", response.calculation_id)
            return response
        result = self._idempotency_store.execute(
            normalize_idempotency_key(idempotency_key),
            request.fingerprint(),
            lambda: self._calculate(request),
        )
        outcome = "idempotent_replay" if result.replayed else "created"
        mark_outcome(outcome, result.response.calculation_id)
        return result.response

    def _calculate(self, request: CalculateRequest) -> CalculationResponse:
        try:
            result = self._service.handle(
                CalculateCommand(request.operand_a, request.operator, request.operand_b)
            )
        except ValueError as error:
            raise DomainCalculationError from error
        return CalculationResponse(
            calculation_id=result.calculation_id,
            operand_a=result.operand_a,
            operator=result.operator,
            operand_b=result.operand_b,
            result=result.result,
        )
