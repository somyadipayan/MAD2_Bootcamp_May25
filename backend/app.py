from flask import Flask, request, jsonify
from models import *
from config import Config
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)

# In a flask application EVERYTHING should run in the current applications context
db.init_app(app)

CORS(app, supports_credentials=True)

# CREATING ADMIN
def create_admin():
    # Check if admin already exists
    existing_librarian = User.query.filter_by(librarian=True).first()
    if existing_librarian:
        return

    # Create admin
    user = User(name="Librarian", email="librarian@library.com", password="1")
    user.librarian = True
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print("Error creating admin:", str(e))


with app.app_context():
    db.create_all()
    create_admin()

@app.route("/", methods=["GET"])
def index():
    return "Hello World"

# REGISTER USER
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")

    # Check if required fields are present
    if not email or not password or not name:
        return jsonify({"error": "Missing required fields"}), 400

    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    # Creating User
    user = User(name=name, email=email, password=password)
    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Something went wrong: " + str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

