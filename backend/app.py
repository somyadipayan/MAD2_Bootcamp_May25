from flask import Flask, request, jsonify
from models import *
from config import Config
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required, unset_jwt_cookies

app = Flask(__name__)
app.config.from_object(Config)

# In a flask application EVERYTHING should run in the current applications context
db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)

CORS(app, supports_credentials=True)

# CREATING ADMIN
def create_admin():
    # Check if admin already exists
    existing_librarian = User.query.filter_by(librarian=True).first()
    if existing_librarian:
        return

    # Create admin
    user = User(name="Librarian", email="librarian@library.com", password= app.config["ADMIN_PASSWORD"])
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
    
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Missing required fields"}), 400
    
    user = User.query.filter_by(email=email).first()
    
    # If user found and password is correct then return token
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity={
            "id": user.id,
            "email": user.email,
            "librarian": user.librarian
        })
        return jsonify({"message": "Login successful", "access_token": access_token}),200

    return jsonify({"error": "Invalid email or password"}), 401 


# @app.route("/books", methods=["GET"])
# @jwt_required()
# def books():
#     user = get_jwt_identity()
#     print(user)
#     return f"{user['email']}-Harry Potter", 200


# @app.route("/add-books", methods=["GET"])
# @jwt_required()
# def add_books():
#     user = get_jwt_identity()
#     if not user['librarian']:
#         return jsonify({"error": "Unauthorized"}), 401
#     return "Hi Admin", 200

@app.route("/get-user-info", methods=["POST"])
@jwt_required()
def get_user_info():
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user['id']).first()

    user_data = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "librarian": user.librarian
    }

    return jsonify({"user": user_data}), 200

@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = jsonify({'message': 'Logout successful'})
    unset_jwt_cookies(response)
    return response

if __name__ == "__main__":
    app.run(debug=True)

