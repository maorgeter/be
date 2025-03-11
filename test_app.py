import pytest
from app import app
from database import users_collection

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

# Test GET /get_users
def test_get_users(client):
    response = client.get("/get_users")
    assert response.status_code == 200
    assert isinstance(response.json, list)

# Test POST /create_user
def test_create_user(client):
    response = client.post("/create_user", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "securepassword"
    })
    assert response.status_code == 201
    assert "User created successfully" in response.json["message"]

# Test duplicate user creation
def test_create_duplicate_user(client):
    response = client.post("/create_user", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "securepassword"
    })
    assert response.status_code == 400
    assert "Email already exists" in response.json["error"]

def test_update_user(client):
    user = users_collection.find_one({"email": "test@example.com"})
    user_id = user["id"]

    response = client.post(f"/update_user/{user_id}", json={
        "name": "Updated User",
        "email": "updated@example.com"
    })
    assert response.status_code == 200
    assert "User updated successfully" in response.json["message"]

def test_delete_user(client):
    user = users_collection.find_one({"email": "updated@example.com"})
    user_id = user["id"]

    response = client.delete(f"/delete_user/{user_id}")
    assert response.status_code == 200
    assert "User deleted successfully" in response.json["message"]
