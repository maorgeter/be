from pymongo import MongoClient
import uuid
import time
from werkzeug.security import generate_password_hash

# running on docker:
MONGO_URI = "mongodb://mongo:27017"

# running local:
# MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "be"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
users_collection = db["users"]

def get_all_users():
    return list(users_collection.find({}, {"_id": 0}))  # Excludes MongoDB _id

def get_user_by_id(user_id):
    return users_collection.find_one({"id": user_id}, {"_id": 0})

def create_user(name, email, password):
    if users_collection.find_one({"email": email}):
        return {"error": "Email already exists"}

    user = {
        "id": str(uuid.uuid4()),  # Unique UUID
        "name": name,
        "email": email,
        "password": generate_password_hash(password),  # Secure password
        "created_at": time.time()
    }
    users_collection.insert_one(user)
    return user

def update_user(user_id, name, email):
    result = users_collection.update_one(
        {"id": user_id},
        {"$set": {"name": name, "email": email, "updated_at": time.time()}}
    )
    return result.matched_count > 0

def delete_user(user_id):
    result = users_collection.delete_one({"id": user_id})
    return result.deleted_count > 0
