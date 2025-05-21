from functools import wraps
import os
from flask import Flask, request, jsonify, send_file
from models import *
from config import Config
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required, unset_jwt_cookies
from werkzeug.utils import secure_filename

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


def librarian_required(f):
    @jwt_required()
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user = get_jwt_identity()
        if not current_user['librarian']:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function


with app.app_context():
    db.create_all()
    create_admin()

@app.route("/", methods=["GET"])
def index():
    return "Hello World"


@app.route('/add_initial_data')
def add_initial_data():
    try:
        section1 = Section(name='Fiction', description='Books related to fictional stories')
        section2 = Section(name='Non-Fiction', description='Books related to real-life events or topics')
        section3 = Section(name='Science', description='Books related to scientific topics')
        section4 = Section(name='History', description='Books related to historical events')

        db.session.add_all([section1, section2, section3, section4])
        db.session.commit()

        book1 = Book(name='The Great Gatsby', description='Lorem ipsum dolor sit amet, consectetur adipiscing elit.', author='F. Scott Fitzgerald', section_id=section1.id, pdf_path='math.pdf')
        book2 = Book(name='To Kill a Mockingbird', description='Sed ut perspiciatis unde omnis iste natus error sit voluptatem.', author='Harper Lee', section_id=section1.id, pdf_path='math.pdf')
        book3 = Book(name='1984', description='But I must explain to you how all this mistaken idea of denouncing pleasure and praising.', author='George Orwell', section_id=section1.id, pdf_path='math.pdf')

        book4 = Book(name='The Diary of a Young Girl', description='At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis.', author='Anne Frank', section_id=section2.id, pdf_path='math.pdf')
        book5 = Book(name='Sapiens: A Brief History of Humankind', description='On the other hand, we denounce with righteous indignation.', author='Yuval Noah Harari', section_id=section2.id, pdf_path='math.pdf')
        book6 = Book(name='The Power of Habit', description='Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil.', author='Charles Duhigg', section_id=section2.id, pdf_path='math.pdf')

        book7 = Book(name='A Brief History of Time', description='Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim.', author='Stephen Hawking', section_id=section3.id, pdf_path='math.pdf')
        book8 = Book(name='The Selfish Gene', description='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', author='Richard Dawkins', section_id=section3.id, pdf_path='math.pdf')
        book9 = Book(name='Astrophysics for People in a Hurry', description='Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam.', author='Neil deGrasse Tyson', section_id=section3.id, pdf_path='math.pdf')

        book10 = Book(name='A People\'s History of the United States', description='Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.', author='Howard Zinn', section_id=section4.id, pdf_path='math.pdf')
        book11 = Book(name='The Rise and Fall of the Third Reich', description='Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', author='William L. Shirer', section_id=section4.id, pdf_path='math.pdf')
        book12 = Book(name='Guns, Germs, and Steel', description='Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium.', author='Jared Diamond', section_id=section4.id, pdf_path='math.pdf')

        book13 = Book(name='The Catcher in the Rye', description='At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque.', author='J.D. Salinger', section_id=section1.id, pdf_path='math.pdf')
        book14 = Book(name='The Hobbit', description='Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus.', author='J.R.R. Tolkien', section_id=section1.id, pdf_path='math.pdf')

        db.session.add_all([book1, book2, book3, book4, book5, book6, book7, book8, book9, book10, book11, book12, book13, book14])
        db.session.commit()

        return jsonify({'message': 'Initial data added successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# REGISTER USER
@app.route("/register", methods=["POST"])
def register():
    """
    This is a route toRegister a new user
    
    Parameters:
        name (str): The name of the user
        email (str): The email of the user
        password (str): The password of the user

    Returns:
        dict: A dictionary with a message
    """
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
    """
    Handles user login by verifying credentials and returning a JWT access token.

    Parameters:
        email (str): The email of the user.
        password (str): The password of the user.

    Returns:
        Response: A JSON response containing a message and an access token if login is successful.
                  A JSON response with an error message if login fails due to missing fields or invalid credentials.
    """

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
    """
    This route is used to get the current user's information.

    It requires a POST request with a JSON body containing the access token.
    The access token is obtained after logging in.

    Returns a JSON object with the user's information like name, email, id and librarian status.

    :return: A JSON object with user's information
    :rtype: JSON
    """
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
    """
    This route is used to log out the current user.

    It requires a POST request and deletes the access token from the cookies.

    Returns a JSON object with a message saying Logout successful.

    :return: A JSON object with a message
    :rtype: JSON
    """
    response = jsonify({'message': 'Logout successful'})
    unset_jwt_cookies(response)
    return response


#############################################################################
######################### CRUD ON SECTIONS ##################################
#############################################################################

@app.route("/add-section", methods=["POST"])
@librarian_required
def add_section():
    """
    Adds a new section to the library.

    This endpoint is only accessible to users with librarian privileges.
    It requires a POST request with a JSON body containing the section's name
    and an optional description.

    If the section name is missing, a 400 error is returned.
    If the section already exists, a message indicating so is returned with a 200 status.
    On successful addition, a message is returned with a 201 status.
    In case of any database errors, a 500 error is returned.

    Returns:
        Response: A JSON response containing a message and appropriate status code.
    """

    data = request.get_json()
    name = data.get("name")
    description = data.get("description")

    if not name:
        return jsonify({"error": "Missing required fields"}), 400
    
    existing_section = Section.query.filter_by(name=name).first()
    if existing_section:
        return jsonify({"message": "Section already exists"}), 200

    section = Section(name=name, description=description)
    try:
        db.session.add(section)
        db.session.commit()
        return jsonify({"message": "Section added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Something went wrong: " + str(e)}), 500

@app.route("/sections", methods=["GET"])
def get_sections():
    sections = Section.query.all()
    section_data = []
    for section in sections:
        books = section.books
        book_data = []
        for book in books:
            book_data.append({
            "id": book.id,
            "name": book.name,
            "author": book.author,
            "description": book.description,
            "pdf_path": book.pdf_path,
            "available": book.available,
            })
        section_data.append({
            "id": section.id,
            "name": section.name,
            "description": section.description,
            "books": book_data
        })
    return jsonify({"sections": section_data}), 200

@app.route("/sections/<int:section_id>", methods=["GET"])
def get_section(section_id):
    section = Section.query.get_or_404(section_id)
    books = section.books
    books_data = []

    for book in books:
        books_data.append({
            "id": book.id,
            "name": book.name,
            "author": book.author,
            "description": book.description,
            "pdf_path": book.pdf_path,
            "available": book.available,
        })

    section_data = {
        "id": section.id,
        "name": section.name,
        "description": section.description,
        "books": books_data
    }
    return jsonify({"section": section_data}), 200

@app.route("/sections/<int:section_id>", methods=["PUT"])
@librarian_required
def update_section(section_id):
    """
    This route is used to update a section.

    It requires a PUT request with a JSON body containing the new name and description of the section.

    If the section name already exists, it will return an error message.

    If the section is updated successfully, it will return a success message.

    :param section_id: The id of the section to be updated
    :return: A JSON object with the result of the operation
    :rtype: JSON
    """
    section = Section.query.get_or_404(section_id)
    data = request.get_json()

    existing_section = Section.query.filter_by(name=data.get("name")).first()
    if existing_section and existing_section.id != section_id:
        return jsonify({"error": "Section name already exists"}), 400

    section.name = data.get("name", section.name)
    section.description = data.get("description", section.description)
    try:
        db.session.commit()
        return jsonify({"message": "Section updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Something went wrong: " + str(e)}), 500
    
@app.route("/sections/<int:section_id>", methods=["DELETE"])
@librarian_required
def delete_section(section_id):
    section = Section.query.get_or_404(section_id)
    try:
        db.session.delete(section)
        db.session.commit()
        return jsonify({"message": "Section deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Something went wrong: " + str(e)}), 500


############################################################################
############################## CRUD ON BOOKS ###############################
############################################################################

# Route for adding a book
# We will be adding a book to a particular section
                # name: '',
                # description: '',
                # author: '',
                # section_id: this.$route.query.section_id,
                # pdf: null
                # data = request.form
                # name = data.get("name")
                # pdf_file = request.files.get("pdf")

    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # name = db.Column(db.String(80), nullable=False)
    # author = db.Column(db.String(80), nullable=False)
    # description = db.Column(db.Text, nullable=True)
    # section_id = db.Column(db.Integer, db.ForeignKey('section.id', ondelete='CASCADE'), nullable=False)
    # pdf_path = db.Column(db.String(120), nullable=True)

@app.route("/add-book", methods=["POST"])
@librarian_required
def add_book():
    data = request.form
    name = data.get("name")
    author = data.get("author")
    description = data.get("description")
    section_id = data.get("section_id")
    pdf_file = request.files.get("pdf")

    if not name or not author or not section_id:
        return jsonify({"error": "Missing required fields"}), 400
    

    # Existing book check if book name and author name already exists
    existing_book = Book.query.filter_by(name=name, author=author).first()
    if existing_book:
        return jsonify({"error": "Book already exists"}), 400
   
    pdf_filename = secure_filename(name+".pdf")
    pdf_path = os.path.join(app.config["UPLOAD_FOLDER"], pdf_filename)

    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    pdf_file.save(pdf_path)

    book = Book(name=name, author=author, description=description, section_id=section_id, pdf_path=pdf_filename)

    try:
        db.session.add(book)
        db.session.commit()
        return jsonify({"message": "Book added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Something went wrong: " + str(e)}), 500

@app.route('/books/<int:id>', methods=['PUT'])
@librarian_required
def update_book(id):    
    book = Book.query.get(id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404

    data = request.json
    name = data.get('name')
    description = data.get('description')
    author = data.get('author')
    section_id = data.get('section_id')

    if not name or not author or not section_id:
        return jsonify({'error': 'Name, author and section_id are required'}), 400
    
    section = Section.query.get(section_id)
    if not section:
        return jsonify({'error': 'Section not found'}), 404
    
    book.name = name
    book.description = description
    book.author = author
    book.section_id = section.id
    db.session.commit()
    return  jsonify({'message': 'Book Updated'}),200

# Delete Book API
@app.route('/books/<int:id>', methods=['DELETE'])
@librarian_required
def delete_book(id):    
    book = Book.query.get(id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    
    db.session.delete(book)
    db.session.commit()

    return jsonify({'message': 'Book deleted'}), 200


# API endpoint to view a book
@app.route('/books/<int:id>', methods=['GET'])
def view_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    
    return jsonify({
        'id': book.id,
        'name': book.name,
        'author': book.author,
        'available': book.available,
        'section_name': book.section.name,
        'section_id': book.section_id,
        'description': book.description
    }), 200


@app.route('/view-pdf/<int:id>', methods=['GET'])
def view_pdf(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    
    pdf_path = os.path.join(app.config["UPLOAD_FOLDER"], book.pdf_path)
    return send_file(pdf_path, mimetype='application/pdf')

if __name__ == "__main__":
    app.run(debug=True)


