import pytest
from fastapi.testclient import TestClient


def test_calculate_via_api(client: TestClient) -> None:
    response = client.post(
        "/api/v1/calculations",
        json={"operand_a": 8, "operator": "divide", "operand_b": 2},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["result"] == 4
    assert body["operator"] == "divide"
    assert body["calculation_id"]


def test_openapi_spec_available(client: TestClient) -> None:
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert "/api/v1/calculations" in response.json().get("paths", {})


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
