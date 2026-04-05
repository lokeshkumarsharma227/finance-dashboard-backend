def test_dashboard_as_analyst(client, analyst_token):
    response = client.get(
        "/api/v1/dashboard/summary",
        headers={"Authorization": f"Bearer {analyst_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "total_income" in data
    assert "total_expenses" in data
    assert "net_balance" in data
    assert "category_totals" in data
    assert "total_records" in data


def test_dashboard_as_viewer_forbidden(client, viewer_token):
    response = client.get(
        "/api/v1/dashboard/summary",
        headers={"Authorization": f"Bearer {viewer_token}"}
    )
    assert response.status_code == 403


def test_dashboard_calculations(client, analyst_token):
    # Create income record
    client.post("/api/v1/records/", json={
        "amount": 10000.0,
        "transaction_type": "income",
        "category": "salary",
        "date": "2024-02-01"
    }, headers={"Authorization": f"Bearer {analyst_token}"})

    # Create expense record
    client.post("/api/v1/records/", json={
        "amount": 3000.0,
        "transaction_type": "expense",
        "category": "rent",
        "date": "2024-02-02"
    }, headers={"Authorization": f"Bearer {analyst_token}"})

    # Check dashboard
    response = client.get(
        "/api/v1/dashboard/summary",
        headers={"Authorization": f"Bearer {analyst_token}"}
    )
    data = response.json()
    assert data["total_income"] >= 10000.0
    assert data["total_expenses"] >= 3000.0
    assert data["net_balance"] == data["total_income"] - data["total_expenses"]


def test_dashboard_without_token(client):
    response = client.get("/api/v1/dashboard/summary")
    assert response.status_code == 401


def test_dashboard_category_totals(client, analyst_token):
    response = client.get(
        "/api/v1/dashboard/summary",
        headers={"Authorization": f"Bearer {analyst_token}"}
    )
    data = response.json()
    assert isinstance(data["category_totals"], list)
    for item in data["category_totals"]:
        assert "category" in item
        assert "total" in item