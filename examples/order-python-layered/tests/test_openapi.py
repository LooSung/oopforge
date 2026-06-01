def test_openapi_spec_available(client) -> None:
    response = client.get("/openapi.json")
    assert response.status_code == 200
    body = response.json()
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
    assert response.json()["order_id"]
