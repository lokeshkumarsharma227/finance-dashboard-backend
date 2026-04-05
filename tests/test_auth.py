def test_register_success(client):
    response = client.post("/api/v1/auth/register", json={
        "full_name": "New User",
        "email": "newuser@test.com",
        "password": "test123",
        "role": "viewer"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newuser@test.com"
    assert data["role"] == "viewer"
    assert "hashed_password" not in data  # security check


def test_register_duplicate_email(client):
    # Register same email twice
    client.post("/api/v1/auth/register", json={
        "full_name": "User One",
        "email": "duplicate@test.com",
        "password": "test123",
        "role": "viewer"
    })
    response = client.post("/api/v1/auth/register", json={
        "full_name": "User Two",
        "email": "duplicate@test.com",
        "password": "test123",
        "role": "viewer"
    })
    assert response.status_code == 400


def test_login_success(client):
    # Register first
    client.post("/api/v1/auth/register", json={
        "full_name": "Login User",
        "email": "loginuser@test.com",
        "password": "test123",
        "role": "viewer"
    })
    # Then login
    response = client.post("/api/v1/auth/login", data={
        "username": "loginuser@test.com",
        "password": "test123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    response = client.post("/api/v1/auth/login", data={
        "username": "loginuser@test.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401


def test_login_wrong_email(client):
    response = client.post("/api/v1/auth/login", data={
        "username": "nobody@test.com",
        "password": "test123"
    })
    assert response.status_code == 401