from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# -------- MYSQL CONNECTION (SEPARATE DB) --------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="NITHISHELANGo@06",
    database="auth_db"
)

# -------- REGISTER --------
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    name = data.get("name")
    mobile = data.get("mobile")
    email = data.get("email")

    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (name, mobile, email) VALUES (%s, %s, %s)",
            (name, mobile, email)
        )
        db.commit()
        return jsonify({"status": "success"})
    except mysql.connector.Error:
        return jsonify({"status": "fail", "message": "User already exists"})
    finally:
        cursor.close()

# -------- LOGIN --------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    name = data.get("name")
    mobile = data.get("mobile")

    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM users WHERE name=%s AND mobile=%s",
        (name, mobile)
    )
    user = cursor.fetchone()
    cursor.close()

    if user:
        return jsonify({"status": "success", "user": user})
    else:
        return jsonify({"status": "fail", "message": "Invalid credentials"})

# -------- START SERVER --------
if __name__ == "__main__":
    app.run(debug=True)
