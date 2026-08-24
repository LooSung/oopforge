from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from app.application.outbox import CalculationPerformedV1
from app.core.dependencies import (
    get_audit_log,
    get_calculate_service,
    get_outbox,
)
from app.infrastructure.event_relay import IdempotentConsumer, OutboxRelay


def calculation_body(operand_a=8, operator="divide", operand_b=2) -> dict:
    return {
        "operand_a": operand_a,
        "operator": operator,
        "operand_b": operand_b,
    }


def test_invalid_input_has_safe_custom_error_and_audit(client) -> None:
    response = client.post(
        "/calculations",
        json={**calculation_body(operator="power"), "secret": "raw-super-secret"},
        headers={"Authorization": "Bearer token-secret", "X-API-Key": "api-secret"},
    )

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"
    correlation_id = response.headers["X-Correlation-Id"]
    assert response.json()["error"]["correlation_id"] == correlation_id
    assert get_audit_log().entries()[0].correlation_id == correlation_id
    exposed = f"{response.json()} {get_audit_log().entries()}"
    assert "raw-super-secret" not in exposed
    assert "token-secret" not in exposed
    assert "api-secret" not in exposed


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
    response = client.post("/calculations", json=payload)

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"


def test_duplicate_normalized_request_returns_first_result_once(client) -> None:
    first = client.post(
        "/calculations",
        json=calculation_body(operand_a=8, operand_b=2),
        headers={"Idempotency-Key": "calculation-1"},
    )
    duplicate = client.post(
        "/calculations",
        json=calculation_body(operand_a=8.0, operand_b=2.0),
        headers={"Idempotency-Key": "calculation-1"},
    )

    assert first.status_code == duplicate.status_code == 201
    assert duplicate.json() == first.json()
    assert len(get_outbox().unpublished()) == 1


def test_duplicate_request_produces_one_relay_effect(client) -> None:
    headers = {"Idempotency-Key": "calculation-2"}
    client.post("/calculations", json=calculation_body(), headers=headers)
    client.post("/calculations", json=calculation_body(), headers=headers)
    effects: list[CalculationPerformedV1] = []

    relayed = OutboxRelay(get_outbox(), IdempotentConsumer(effects.append)).relay()

    assert relayed == 1
    assert len(effects) == 1


def test_reused_key_with_different_body_returns_safe_conflict(client) -> None:
    headers = {"Idempotency-Key": "calculation-3"}
    client.post("/calculations", json=calculation_body(), headers=headers)
    response = client.post(
        "/calculations",
        json=calculation_body(operand_b=4),
        headers=headers,
    )

    assert response.status_code == 409
    assert response.json()["error"]["code"] == "idempotency_conflict"
    assert set(response.json()) == {"error"}
    assert len(get_outbox().unpublished()) == 1


def test_division_by_zero_has_safe_domain_error(client) -> None:
    response = client.post(
        "/calculations",
        json=calculation_body(operand_a=1, operand_b=0),
    )

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "calculation_rejected"
    assert "division" not in str(response.json()).lower()
    assert get_outbox().unpublished() == ()


def test_generates_correlation_id_and_audits_it(client) -> None:
    response = client.post("/calculations", json=calculation_body())
    correlation_id = response.headers["X-Correlation-Id"]
    entry = get_audit_log().entries()[0]

    assert UUID(correlation_id)
    assert entry.correlation_id == correlation_id
    assert entry.calculation_id == response.json()["calculation_id"]
    assert entry.action == "create_calculation"
    assert entry.outcome == "created"


def test_preserves_valid_provided_correlation_id(client) -> None:
    response = client.post(
        "/calculations",
        json=calculation_body(),
        headers={"X-Correlation-Id": "request-123"},
    )

    assert response.status_code == 201
    assert response.headers["X-Correlation-Id"] == "request-123"
    assert get_audit_log().entries()[0].correlation_id == "request-123"


def test_unexpected_failure_has_no_internal_detail(client, monkeypatch) -> None:
    def fail(_):
        raise RuntimeError("database password is internal-secret")

    monkeypatch.setattr(get_calculate_service(), "handle", fail)
    response = client.post("/calculations", json=calculation_body())

    assert response.status_code == 500
    assert response.json()["error"]["code"] == "internal_error"
    assert "internal-secret" not in str(response.json())
    assert "RuntimeError" not in str(response.json())
