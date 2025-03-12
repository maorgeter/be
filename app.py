from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import get_all_users, get_user_by_id, create_user, update_user, delete_user
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from prometheus_flask_exporter import PrometheusMetrics
from flasgger import Swagger

app = Flask(__name__)

# JWT Configuration
app.config["JWT_SECRET_KEY"] = "maorsmartech" 
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)

metrics = PrometheusMetrics(app, path="/metrics")
swagger = Swagger(app)

get_users_counter = metrics.counter("get_users_requests", "Count of get users requests")
user_creation_counter = metrics.counter("user_creation_requests", "Count of user creation requests")
user_deletion_counter = metrics.counter("user_deletion_requests", "Count of user deletion requests")
user_update_counter = metrics.counter("user_update_requests", "Count of user update requests")

request_latency = metrics.histogram(
    "flask_request_latency_seconds", "Histogram for request latency",
    labels={"endpoint": lambda: request.path}
)

# Hardcoded Admin Credentials
ADMIN_CREDENTIALS = {"email": "maor@geter.com", "password": "smartech"}

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
    users = get_all_users()
    return render_template("index.html", users=users)

@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    """
    Admin Login
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
            password:
              type: string
    responses:
      200:
        description: Login successful (Returns JWT token)
      401:
        description: Invalid credentials
    """
    if request.method == "GET":
        return render_template("admin_login.html")  # Serve login page

    # If POST request → process login
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if email == ADMIN_CREDENTIALS["email"] and password == ADMIN_CREDENTIALS["password"]:
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token), 200

    return jsonify({"error": "Invalid credentials"}), 401


@app.route("/get_users", methods=["GET"])
@jwt_required()
@get_users_counter
def get_users():
    return jsonify(get_all_users()), 200

@app.route("/create_user", methods=["POST"])
@jwt_required()
@user_creation_counter
@request_latency
def add_user():
    data = request.json
    if not data.get("name") or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Name, email, and password are required"}), 400

    user = create_user(data["name"], data["email"], data["password"])
    return jsonify(user), 201

@app.route("/update_user/<user_id>", methods=["PUT"])
@jwt_required()
@user_update_counter
@request_latency
def modify_user(user_id):
    data = request.json
    if not data.get("name") or not data.get("email"):
        return jsonify({"error": "Name and email are required"}), 400

    if update_user(user_id, data["name"], data["email"]):
        return jsonify({"message": "User updated successfully"}), 200
    return jsonify({"error": "User not found"}), 404

@app.route("/delete_user/<user_id>", methods=["DELETE"])
@jwt_required()
@user_deletion_counter
@request_latency
def remove_user(user_id):
    if delete_user(user_id):
        return jsonify({"message": "User deleted successfully"}), 200
    return jsonify({"error": "User not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
