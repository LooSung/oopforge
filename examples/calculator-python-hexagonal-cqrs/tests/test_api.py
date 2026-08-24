import pytest
from fastapi.testclient import TestClient

from app.presentation.api.schemas import HistoryEntryResponse


def test_calculate_and_read_history_via_api(client: TestClient) -> None:
    created = client.post(
        "/api/v1/calculations",
        json={"operand_a": 8, "operand_b": 2, "operator": "divide"},
    )
    assert created.status_code == 201
    calculation_id = created.json()["calculation_id"]

    history = client.get("/api/v1/calculations/history")
    assert history.status_code == 200
    assert history.json()["items"][0]["result"] == 4

    one = client.get(f"/api/v1/calculations/{calculation_id}")
    assert one.status_code == 200
    assert one.json()["operator"] == "divide"


def test_history_schema_preserves_datetime_format() -> None:
    performed_at = HistoryEntryResponse.model_json_schema()["properties"]["performed_at"]

    assert performed_at["format"] == "date-time"


@pytest.mark.parametrize(
    "payload",
    [
        {"operand_a": 8, "operator": "divide"},
        {"operand_a": None, "operator": "divide", "operand_b": 2},
        {"operand_a": 8, "operator": "divide", "operand_b": 2, "extra": True},
        {"operand_a": "8", "operator": "divide", "operand_b": 2},
        {"operand_a": 8, "operator": "power", "operand_b": 2},
        {"operand_a": "NaN", "operator": "add", "operand_b": 2},
    ],
)
def test_rejects_values_outside_request_contract(
    client: TestClient, payload: dict[str, object]
) -> None:
    response = client.post("/api/v1/calculations", json=payload)

    assert response.status_code == 422
