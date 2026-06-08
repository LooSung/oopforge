def test_calculate_and_read_history_via_api(client) -> None:
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
