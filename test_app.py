import pytest
from app import app, ADMIN_CREDENTIALS
from database import users_collection
from bson import ObjectId

def convert_object_id(obj):
    """Recursively convert ObjectId fields to strings for JSON serialization."""
    if isinstance(obj, dict):
        return {key: convert_object_id(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_object_id(item) for item in obj]
    elif isinstance(obj, ObjectId):
        return str(obj)  # Convert ObjectId to string
    return obj

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def auth_token(client):
    """Logs in as admin and retrieves JWT token."""
    response = client.post("/admin_login", json={
        "email": ADMIN_CREDENTIALS["email"],
        "password": ADMIN_CREDENTIALS["password"]
    })
    assert response.status_code == 200
    return response.json["access_token"]

@pytest.fixture(autouse=True)
def clean_test_users():
    """Removes test users before and after each test to ensure a clean state."""
    users_collection.delete_many({"email": {"$regex": "^test"}})  
    yield
    users_collection.delete_many({"email": {"$regex": "^test"}})

# Test GET /get_users with authentication
def test_get_users(client, auth_token):
    response = client.get("/get_users", headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 200
    assert isinstance(response.json, list)

# Test POST /create_user with authentication
def test_create_user(client, auth_token):
    response = client.post("/create_user", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "securepassword"
    }, headers={"Authorization": f"Bearer {auth_token}"})

    assert response.status_code == 201
    user_data = convert_object_id(response.json) 
    assert "id" in user_data  # Ensure user ID is returned
    assert "test@example.com" == user_data["email"]

# Test PUT /update_user/<user_id> with authentication
def test_update_user(client, auth_token):
    # Create a test user first
    response = client.post("/create_user", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "securepassword"
    }, headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 201

    user = users_collection.find_one({"email": "test@example.com"})
    assert user is not None, "Test user not found in database."
    
    user_id = str(user["id"]) 
    
    response = client.put(f"/update_user/{user_id}", json={
        "name": "Updated User",
        "email": "updated@example.com"
    }, headers={"Authorization": f"Bearer {auth_token}"})

    assert response.status_code == 200
    updated_data = convert_object_id(response.json)  # ✅ Convert ObjectId to string
    assert "User updated successfully" in updated_data["message"]

def test_delete_user(client, auth_token):
    # Create a test user first
    response = client.post("/create_user", json={
        "name": "Test User",
        "email": "test@delete.com",
        "password": "securepassword"
    }, headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 201

    # Retrieve user from DB
    user = users_collection.find_one({"email": "test@delete.com"})
    assert user is not None, "Test user not found in database."

    user_id = str(user["id"])  # ✅ Ensure ID is a string

    response = client.delete(f"/delete_user/{user_id}", headers={"Authorization": f"Bearer {auth_token}"})
    
    assert response.status_code == 200
    deleted_data = convert_object_id(response.json)  # ✅ Convert ObjectId to string
    assert "User deleted successfully" in deleted_data["message"]
