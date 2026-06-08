def test_calculate_via_api(client) -> None:
    response = client.post(
        "/api/v1/calculations",
        json={"operand_a": 8, "operator": "divide", "operand_b": 2},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["result"] == 4
    assert body["operator"] == "divide"
    assert body["calculation_id"]


def test_openapi_spec_available(client) -> None:
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert "/api/v1/calculations" in response.json().get("paths", {})
