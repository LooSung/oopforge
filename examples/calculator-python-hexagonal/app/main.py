from fastapi import FastAPI, Request, Response
from starlette.middleware.base import RequestResponseEndpoint

from app.core.dependencies import get_audit_log
from app.presentation.api.errors import install_error_handlers
from app.presentation.api.calculation.router import router as calculation_router
from app.presentation.api.production import observe_request

app = FastAPI(title="OOPforge Calculator (FastAPI hexagonal)")
install_error_handlers(app)
app.include_router(calculation_router)


@app.middleware("http")
async def production_readiness(
    request: Request,
    call_next: RequestResponseEndpoint,
) -> Response:
    return await observe_request(request, call_next, get_audit_log())
