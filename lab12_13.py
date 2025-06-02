from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required,
    get_jwt_identity, get_jwt
)
from datetime import timedelta

app = Flask(__name__)


app.config["JWT_SECRET_KEY"] = "parola"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)


users = {
    "user1": {"password": "parola1", "role": "admin"},
    "user2": {"password": "parola2", "role": "owner"},
    "user3": {"password": "parolaX", "role": "owner"}
}

revoked_tokens = set()

@app.route("/auth", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = users.get(username)
    if user and user["password"] == password:
        token = create_access_token(identity={"username": username, "role": user["role"]})
        return jsonify(access_token=token), 200
    return jsonify({"msg": "Invalid credentials"}), 401


@app.route("/auth/jwtStore", methods=["GET"])
@jwt_required()
def verify_token():
    identity = get_jwt_identity()
    return jsonify(role=identity["role"]), 200


@app.route("/auth/jwtStore", methods=["DELETE"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    revoked_tokens.add(jti)
    return jsonify(msg="Token revoked"), 200


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    return jwt_payload["jti"] in revoked_tokens


@app.route("/sensor-data", methods=["GET"])
@jwt_required()
def read_sensor_data():
    identity = get_jwt_identity()
    if identity["role"] in ["owner", "admin"]:
        return jsonify(data="Valoarea senzorului: 32"), 200
    return jsonify({"msg": "Access denied"}), 403

@app.route("/sensor-config", methods=["POST"])
@jwt_required()
def update_sensor_config():
    identity = get_jwt_identity()
    if identity["role"] == "admin":
        return jsonify(msg="Configurare actualizată cu succes"), 200
    return jsonify({"msg": "Access denied"}), 403

if __name__ == "__main__":
    app.run(debug=True)