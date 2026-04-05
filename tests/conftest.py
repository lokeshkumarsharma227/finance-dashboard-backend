import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base
from app.db.session import get_db
from main import app

# Test database — separate from real database
SQLALCHEMY_TEST_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Create all tables in test database
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# Override real DB with test DB
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


# Test client fixture
@pytest.fixture(scope="module")
def client():
    return TestClient(app)


# Auth token fixture — registers and logs in admin
@pytest.fixture(scope="module")
def admin_token(client):
    # Register admin
    client.post("/api/v1/auth/register", json={
        "full_name": "Test Admin",
        "email": "testadmin@test.com",
        "password": "test123",
        "role": "admin"
    })
    # Login
    response = client.post("/api/v1/auth/login", data={
        "username": "testadmin@test.com",
        "password": "test123"
    })
    return response.json()["access_token"]


# Analyst token fixture
@pytest.fixture(scope="module")
def analyst_token(client):
    client.post("/api/v1/auth/register", json={
        "full_name": "Test Analyst",
        "email": "testanalyst@test.com",
        "password": "test123",
        "role": "analyst"
    })
    response = client.post("/api/v1/auth/login", data={
        "username": "testanalyst@test.com",
        "password": "test123"
    })
    return response.json()["access_token"]


# Viewer token fixture
@pytest.fixture(scope="module")
def viewer_token(client):
    client.post("/api/v1/auth/register", json={
        "full_name": "Test Viewer",
        "email": "testviewer@test.com",
        "password": "test123",
        "role": "viewer"
    })
    response = client.post("/api/v1/auth/login", data={
        "username": "testviewer@test.com",
        "password": "test123"
    })
    return response.json()["access_token"]