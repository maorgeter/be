from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import uuid
import time
import os
from werkzeug.security import generate_password_hash, check_password_hash

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "be"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
users_collection = db["users"]
users_collection.create_index("email", unique=True)


def get_all_users():
    return list(users_collection.find({}, {"_id": 0}))  # Excludes MongoDB _id

def get_user_by_id(user_id):
    return users_collection.find_one({"id": user_id}, {"_id": 0})

def create_user(name, email, password):
    if users_collection.find_one({"email": email}):
        return {"error": "Email already exists"}
    print("**********")
    print(email)

    user = {
        "id": str(uuid.uuid4()),  # Unique UUID
        "name": name,
        "email": email,
        "password": generate_password_hash(password),  # Secure password
        "created_at": time.time()
    }
    users_collection.insert_one(user)
    user.pop("_id", None)
    return user

def update_user(user_id, name, email):
    try:
        result = users_collection.update_one(
            {"id": user_id},
            {"$set": {"name": name, "email": email, "updated_at": time.time()}}
        )
        if result.matched_count == 0:
            return {"error": "User not found"}
        return {"message": "User updated successfully"}
    except DuplicateKeyError:
        return {"error": "Email already exists"}

def delete_user(user_id):
    result = users_collection.delete_one({"id": user_id})
    return result.deleted_count > 0

def get_user_by_email(email):
    return users_collection.find_one({"email": email}, {"_id": 0})

def check_password(password, hashed_password):
    return check_password_hash(hashed_password, password)