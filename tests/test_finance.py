def test_create_record_as_analyst(client, analyst_token):
    response = client.post("/api/v1/records/", json={
        "amount": 5000.0,
        "transaction_type": "income",
        "category": "salary",
        "date": "2024-01-15",
        "description": "Monthly salary"
    }, headers={"Authorization": f"Bearer {analyst_token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["amount"] == 5000.0
    assert data["category"] == "salary"


def test_create_record_as_viewer_forbidden(client, viewer_token):
    response = client.post("/api/v1/records/", json={
        "amount": 1000.0,
        "transaction_type": "income",
        "category": "salary",
        "date": "2024-01-15"
    }, headers={"Authorization": f"Bearer {viewer_token}"})
    assert response.status_code == 403


def test_get_records(client, analyst_token):
    response = client.get(
        "/api/v1/records/",
        headers={"Authorization": f"Bearer {analyst_token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_filter_records_by_type(client, analyst_token):
    response = client.get(
        "/api/v1/records/filter?transaction_type=income",
        headers={"Authorization": f"Bearer {analyst_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    for record in data:
        assert record["transaction_type"] == "income"


def test_update_record_as_analyst(client, analyst_token):
    # Create record first
    create = client.post("/api/v1/records/", json={
        "amount": 3000.0,
        "transaction_type": "expense",
        "category": "rent",
        "date": "2024-01-20"
    }, headers={"Authorization": f"Bearer {analyst_token}"})
    record_id = create.json()["id"]

    # Update it
    response = client.patch(
        f"/api/v1/records/{record_id}",
        json={"amount": 3500.0},
        headers={"Authorization": f"Bearer {analyst_token}"}
    )
    assert response.status_code == 200
    assert response.json()["amount"] == 3500.0


def test_delete_record_as_viewer_forbidden(client, viewer_token, analyst_token):
    # Create record as analyst
    create = client.post("/api/v1/records/", json={
        "amount": 1000.0,
        "transaction_type": "income",
        "category": "bonus",
        "date": "2024-01-25"
    }, headers={"Authorization": f"Bearer {analyst_token}"})
    record_id = create.json()["id"]

    # Try delete as viewer
    response = client.delete(
        f"/api/v1/records/{record_id}",
        headers={"Authorization": f"Bearer {viewer_token}"}
    )
    assert response.status_code == 403


def test_delete_record_as_admin(client, admin_token, analyst_token):
    # Create record as analyst
    create = client.post("/api/v1/records/", json={
        "amount": 2000.0,
        "transaction_type": "expense",
        "category": "food",
        "date": "2024-01-26"
    }, headers={"Authorization": f"Bearer {analyst_token}"})
    record_id = create.json()["id"]

    # Delete as admin
    response = client.delete(
        f"/api/v1/records/{record_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200