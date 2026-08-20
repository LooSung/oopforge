import logging

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.presentation.api.idempotency import (
    IdempotencyConflict,
    InvalidIdempotencyKey,
)
from app.presentation.api.observability import (
    current_correlation_id,
    mark_outcome,
)


_logger = logging.getLogger("calculator.api")


class DomainCalculationError(Exception):
    pass


def install_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(RequestValidationError, validation_error)
    app.add_exception_handler(InvalidIdempotencyKey, invalid_idempotency_key)
    app.add_exception_handler(IdempotencyConflict, idempotency_conflict)
    app.add_exception_handler(DomainCalculationError, domain_error)
    app.add_exception_handler(Exception, unexpected_error)


async def validation_error(_: Request, __: Exception) -> JSONResponse:
    return _safe_error(
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        "validation_error",
        "Request validation failed",
    )


async def invalid_idempotency_key(_: Request, __: Exception) -> JSONResponse:
    return _safe_error(
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        "validation_error",
        "Request validation failed",
    )


async def idempotency_conflict(_: Request, __: Exception) -> JSONResponse:
    return _safe_error(
        status.HTTP_409_CONFLICT,
        "idempotency_conflict",
        "Idempotency key was already used for another request",
    )


async def domain_error(_: Request, __: Exception) -> JSONResponse:
    return _safe_error(
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        "calculation_rejected",
        "Calculation could not be completed",
    )


async def unexpected_error(_: Request, __: Exception) -> JSONResponse:
    correlation_id = current_correlation_id()
    _logger.error("request_failed", extra={"correlation_id": correlation_id})
    return _safe_error(
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        "internal_error",
        "An unexpected error occurred",
    )


def _safe_error(status_code: int, code: str, message: str) -> JSONResponse:
    correlation_id = current_correlation_id()
    mark_outcome(code)
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": code,
                "message": message,
                "correlation_id": correlation_id,
            }
        },
        headers={"X-Correlation-Id": correlation_id},
    )
