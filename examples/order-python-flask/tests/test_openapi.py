def test_openapi_spec_available(client) -> None:
    response = client.get("/api/v1/openapi.json")
    assert response.status_code == 200
    body = response.get_json()
    assert body is not None
    assert "openapi" in body
    assert "/api/v1/orders" in body.get("paths", {})


def test_place_order_via_api(client) -> None:
    response = client.post(
        "/api/v1/orders",
        json={
            "customer_id": "cust-1",
            "lines": [{"product_id": "p-1", "quantity": 2, "unit_price": 1000}],
        },
    )
    assert response.status_code == 201
    assert response.get_json()["order_id"]
