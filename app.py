from datetime import datetime
from flask import Flask, render_template, request, jsonify
from database import get_all_users, get_user_by_id, create_user, update_user, delete_user

app = Flask(__name__)

@app.template_filter('datetimeformat')
def datetimeformat(value):
    if isinstance(value, datetime):
        return value.strftime('%Y-%m-%d %H:%M:%S')
    try:
        return datetime.utcfromtimestamp(int(value)).strftime('%Y-%m-%d %H:%M:%S')
    except (ValueError, TypeError):
        return "Invalid Date"

@app.route("/get_users", methods=["GET"])
def get_users():
    users = get_all_users()
    return jsonify(users), 200

# duplication of /get_users (for UI)
@app.route("/")
def index():
    users = get_all_users()
    return render_template("index.html", users=users)

@app.route("/create_user", methods=["POST"])
def add_user():
    data = request.json
    if not data.get("name") or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Name, email, and password are required"}), 400

    user = create_user(data["name"], data["email"], data["password"])
    if "error" in user:
        return jsonify(user), 400

    return jsonify({"id": user["id"], "message": "User created successfully"}), 201

@app.route("/update_user/<user_id>", methods=["POST"])
def modify_user(user_id):
    data = request.json
    if not data.get("name") or not data.get("email"):
        return jsonify({"error": "Name and email are required"}), 400

    if update_user(user_id, data["name"], data["email"]):
        return jsonify({"message": "User updated successfully"}), 200
    return jsonify({"error": "User not found"}), 404

@app.route("/delete_user/<user_id>", methods=["DELETE"])
def remove_user(user_id):
    if delete_user(user_id):
        return jsonify({"message": "User deleted successfully"}), 200
    return jsonify({"error": "User not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
