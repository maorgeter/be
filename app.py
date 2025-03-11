from datetime import datetime
import time
import uuid
from flask import Flask, render_template, request, jsonify
from database import users_collection
from bson import ObjectId
from werkzeug.security import generate_password_hash


app = Flask(__name__)

@app.template_filter('datetimeformat')
def datetimeformat(value):
    if isinstance(value, datetime):
        return value.strftime('%Y-%m-%d %H:%M:%S')
    try:
        return datetime.utcfromtimestamp(int(value)).strftime('%Y-%m-%d %H:%M:%S')
    except (ValueError, TypeError):
        return "Invalid Date"

@app.route("/")
def index():
    users = list(users_collection.find({}, {"_id": 0}))
    return render_template("index.html", users=users)

@app.route("/create_user", methods=["POST"])
def add_user():
    data = request.json
    if not data.get("name") or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Name, email, and password are required"}), 400

    # Check if email already exists
    existing_user = users_collection.find_one({"email": data["email"]})
    if existing_user:
        return jsonify({"error": "This email is already registered."}), 400

    user = {
        "id": str(uuid.uuid4()),
        "name": data["name"],
        "email": data["email"],
        "password": generate_password_hash(data["password"]),  # Hash the password
        "created_at": time.time(), 
    }
    users_collection.insert_one(user)
    return jsonify({"id": user["id"], "message": "User created successfully"}), 201

@app.route("/update_user/<user_id>", methods=["POST"])
def update_user(user_id):
    data = request.json

    result = users_collection.update_one(
        {"id": user_id},
        {
            "$set": {
                "name": data["name"],
                "email": data["email"],
                "updated_at": time.time()
            }
        }
    )
    if result.matched_count == 0:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User updated successfully"})

@app.route("/delete_user/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    result = users_collection.delete_one({"id": user_id})
    if result.deleted_count == 0:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User deleted successfully"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
