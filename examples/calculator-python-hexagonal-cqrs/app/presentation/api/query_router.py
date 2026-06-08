from fastapi import APIRouter, Depends, HTTPException, Query

from app.application.query.history_query_service import HistoryQueryService
from app.application.query.history_summary import HistorySummary
from app.core.dependencies import get_query_service
from app.domain.calculation.value import CalculationId
from app.presentation.api.schemas import HistoryEntryResponse, HistoryListResponse

router = APIRouter(prefix="/api/v1/calculations", tags=["Calculator Queries"])


def _to_response(entry: HistorySummary) -> HistoryEntryResponse:
    return HistoryEntryResponse(
        calculation_id=entry.calculation_id,
        operand_a=entry.operand_a,
        operand_b=entry.operand_b,
        operator=entry.operator,
        result=entry.result,
        performed_at=entry.performed_at.isoformat(),
    )


@router.get("/history", response_model=HistoryListResponse)
def list_history(
    limit: int = Query(default=20, ge=1, le=100),
    service: HistoryQueryService = Depends(get_query_service),
) -> HistoryListResponse:
    items = [_to_response(entry) for entry in service.list_recent(limit)]
    return HistoryListResponse(items=items)


@router.get("/{calculation_id}", response_model=HistoryEntryResponse)
def get_calculation(
    calculation_id: str,
    service: HistoryQueryService = Depends(get_query_service),
) -> HistoryEntryResponse:
    entry = service.get_by_id(CalculationId.parse(calculation_id))
    if entry is None:
        raise HTTPException(status_code=404, detail="calculation not found")
    return _to_response(entry)
