import logging

from fastapi import Request, Response
from starlette.middleware.base import RequestResponseEndpoint

from app.presentation.api.audit import AuditEntry, AuditPort
from app.presentation.api.errors import unexpected_error
from app.presentation.api.observability import (
    begin_request,
    choose_correlation_id,
    current_calculation_id,
    current_outcome,
    end_request,
)


_logger = logging.getLogger("calculator.api")


async def observe_request(
    request: Request,
    call_next: RequestResponseEndpoint,
    audit_log: AuditPort,
) -> Response:
    correlation_id = choose_correlation_id(request.headers.get("X-Correlation-Id"))
    tokens = begin_request(correlation_id)
    try:
        response = await _call_safely(request, call_next)
        _record_completion(request, response, audit_log, correlation_id)
        return response
    finally:
        end_request(tokens)


async def _call_safely(
    request: Request,
    call_next: RequestResponseEndpoint,
) -> Response:
    try:
        return await call_next(request)
    except Exception as error:
        return await unexpected_error(request, error)


def _record_completion(
    request: Request,
    response: Response,
    audit_log: AuditPort,
    correlation_id: str,
) -> None:
    response.headers["X-Correlation-Id"] = correlation_id
    entry = AuditEntry(
        action=_safe_action(request),
        outcome=current_outcome(),
        correlation_id=correlation_id,
        calculation_id=current_calculation_id(),
    )
    audit_log.record(entry)
    _logger.info("request_completed", extra=entry.__dict__)


def _safe_action(request: Request) -> str:
    if request.method == "POST" and request.url.path == "/calculations":
        return "create_calculation"
    return "http_request"
